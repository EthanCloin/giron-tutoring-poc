from flask import current_app, g
import sqlite3
import click


def get_db():
    # 'g' is a flask object generated on each unique request.
    # if a single request hits the db multiple times, it would reuse the
    # db already present in 'g'
    if "db" not in g:
        g.db = sqlite3.connect("./booking.db", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()
    with current_app.open_resource("static/sql/build-fresh-schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    with current_app.open_resource("static/sql/add-dummy-data.sql") as f:
        db.executescript(f.read().decode("utf8"))
    # insert_bookings(db)


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def generate_bookings(all_tutors_availability):
    """accept the tutoravailability data and return 30 days worth of time slots"""
    from datetime import datetime, timezone, timedelta

    # TODO: support override dates
    # TODO: solve the timezone bug throwing off dates in default availability ISSUE #6
    bookings = []
    for i in range(31):
        next_day = datetime.now(timezone.utc) + timedelta(days=i)
        avail_this_weekday = [
            a for a in all_tutors_availability if a.get("DayUTC") == next_day.weekday()
        ]
        for avail in avail_this_weekday:
            hour, minute = avail.get("TimeUTC").split(":")
            timeslot = datetime(
                year=next_day.year,
                month=next_day.month,
                day=next_day.day,
                hour=int(hour),
                minute=int(minute),
                tzinfo=timezone.utc,
            )
            booking_entry = {
                "TutorAvailabilityID": avail.get("TutorAvailabilityID"),
                "TimeSlot": timeslot.isoformat(),
            }
            bookings.append(booking_entry)
    return [x for x in bookings if len(x) > 0]


def insert_bookings(db: sqlite3.Connection):
    """use the contents of TutorAvailability to build Booking values"""
    ta = [dict(x) for x in db.execute("SELECT * FROM TutorAvailability").fetchall()]
    bookings = [
        (b.get("TutorAvailabilityID"), b.get("TimeSlot")) for b in generate_bookings(ta)
    ]

    db.executemany(
        "INSERT INTO Bookings (TutorAvailabilityID, TimeSlot) VALUES (?, ?)", bookings
    )
    db.commit()


if __name__ == "__main__":
    pass

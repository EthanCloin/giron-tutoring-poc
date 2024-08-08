from flask import Blueprint, request, render_template, jsonify
from app.database import get_db
from datetime import datetime, timezone, timedelta


bp = Blueprint("bookings", __name__, url_prefix="/bookings")


@bp.route("/<tutor_id>/create", methods=["POST"])
def generate_bookings(tutor_id):
    """accept the tutoravailability data and create 30 days worth of time slots
    return the dates for those bookings for use in smart-calendar component
    """

    # TODO: support override dates
    # TODO: solve the timezone bug throwing off dates in default availability ISSUE #6
    # https://blogs.oracle.com/javamagazine/post/java-timezone-part-1
    # plan: generate this based on client request which includes request date and
    # and cache unless updated by tutor
    db = get_db()
    request_time_iso = request.form.to_dict()["requestTime"]
    print("req time: ", request_time_iso)
    request_date = parse_iso(request_time_iso)

    if bookings_are_generated(tutor_id, request_date):
        return get_booking_dates(tutor_id)
    # TODO: drop previously built bookings

    query = """
SELECT TutorAvailabilityID, DayUTC, TimeUTC
FROM TutorAvailability
WHERE TutorID = ?"""
    tutor_availability = [dict(ta) for ta in db.execute(query, (tutor_id,)).fetchall()]

    bookings = build_booking_entries(request_date, tutor_availability)

    db.executemany(
        "INSERT INTO Bookings (TutorAvailabilityID, TimeSlot) VALUES (?, ?)", bookings
    )
    db.commit()
    mark_bookings_generated(tutor_id, request_date)

    return get_booking_dates(tutor_id)


@bp.route("/<tutor_id>/time-slots", methods=["GET"])
def get_time_slots(tutor_id):

    db = get_db()
    request_data = request.args
    selected_date = parse_iso(request_data["selectedDate"])
    # tutor_id = int(request_data["tutorID"])

    # TODO: cache query result in Flask request or q or wherever
    query = """
SELECT b.BookingID, b.TimeSlot
FROM Bookings b
JOIN TutorAvailability ta ON ta.TutorAvailabilityID = b.TutorAvailabilityID
JOIN Tutors t ON ta.TutorID = t.TutorID
WHERE t.TutorID = ?"""
    bookings = [dict(r) for r in db.execute(query, (tutor_id,)).fetchall()]
    # pprint(bookings)
    time_slots = [
        b
        for b in bookings
        if in_display_range(selected_date, parse_iso(b.get("TimeSlot")))
    ]
    mapped_time_slots = map_time_slots_to_days(selected_date, time_slots)

    return render_template("time-slots.html", time_slots=mapped_time_slots)


@bp.route("/", methods=["GET"])
def booking_form_view():
    booking_id = request.form.to_dict()["bookingID"]
    print(booking_id)
    db = get_db()
    query = """
SELECT b.BookingID,
    b.TimeSlot,
    t.Name AS TutorName,
    t.Email
FROM Bookings b
    JOIN TutorAvailability ta ON b.TutorAvailabilityID = ta.TutorAvailabilityID
    JOIN Tutors t ON t.TutorID = ta.TutorID
WHERE b.BookingID = ?
"""
    booking_and_tutor = dict(db.execute(query, (booking_id,)).fetchone())
    return render_template("booking_form.html", booking=booking_and_tutor)


def get_booking_dates(tutor_id):
    db = get_db()
    query = """
SELECT b.BookingID, b.TimeSlot
FROM Bookings b
JOIN TutorAvailability ta ON ta.TutorAvailabilityID = b.TutorAvailabilityID
JOIN Tutors t ON ta.TutorID = t.TutorID
WHERE t.TutorID = ?"""
    times = [dict(r).get("TimeSlot") for r in db.execute(query, (tutor_id,)).fetchall()]
    # unique list YYYY-MM-DD
    days = list(set([parse_iso(t).date().isoformat() for t in times]))
    return jsonify(days)


def build_booking_entries(request_day: datetime, tutor_availability):
    bookings = []
    for i in range(31):
        next_day = request_day + timedelta(days=i)
        avail_this_weekday = [
            a
            for a in tutor_availability
            if a.get("DayUTC") == map_py_weekday_to_utc_day(next_day.weekday())
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
    return [
        (b.get("TutorAvailabilityID"), b.get("TimeSlot"))
        for b in bookings
        if len(b) > 0
    ]


def bookings_are_generated(tutor_id, request_date: datetime):
    db = get_db()
    # TODO: delete row here if current date doesn't match LastGenerated
    get_cached_query = "SELECT LastGenerated FROM BookingsCache WHERE TutorID = ?"
    found_time = db.execute(get_cached_query, (tutor_id,)).fetchone()

    if found_time:
        found_time = datetime.fromisoformat(
            dict(found_time).get("LastGenerated")
        ).astimezone(timezone.utc)
        return found_time.date() == request_date.date()


def mark_bookings_generated(tutor_id, request_date: datetime):
    db = get_db()
    insert_query = (
        "INSERT OR REPLACE INTO BookingsCache (TutorID, LastGenerated) VALUES (?, ?)"
    )
    db.execute(insert_query, (tutor_id, request_date.isoformat()))
    db.commit()


def parse_iso(iso_string) -> datetime:
    if iso_string.endswith("Z"):
        iso_string = iso_string[:-1] + "+00:00"
    return datetime.fromisoformat(iso_string)


def map_py_weekday_to_utc_day(weekday: int) -> int:
    PY_TO_UTC = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 0}
    return PY_TO_UTC[weekday]


def in_display_range(selected_date: datetime, other_date: datetime) -> bool:
    difference = abs(selected_date.date() - other_date.date()).days
    print(f"{selected_date.date()} is {difference} from {other_date.date()}")
    return difference <= 1


def map_time_slots_to_days(selected_date: datetime, time_slots):

    mapped = {"previous": [], "selected": [], "after": []}
    before_selected = selected_date.date() - timedelta(days=1)
    after_selected = selected_date.date() + timedelta(days=1)
    for ts in time_slots:
        cur_date = parse_iso(ts.get("TimeSlot")).date()
        if cur_date == before_selected:
            mapped["previous"].append(ts)
        elif cur_date == after_selected:
            mapped["after"].append(ts)
        elif cur_date == selected_date.date():
            mapped["selected"].append(ts)
        else:
            raise ValueError(
                f"{cur_date} is not within 1 day of selected {selected_date.date()}"
            )
    return mapped

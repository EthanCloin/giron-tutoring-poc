from re import T
from wsgiref.util import request_uri
from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    request,
    render_template,
    url_for,
    session,
)
from app.database import get_db
from datetime import datetime, timezone, timedelta
from pprint import pprint


bp = Blueprint("bookings", __name__, url_prefix="/bookings")


@bp.route("/<tutor_id>/time-slots", methods=["GET"])
def get_time_slots(tutor_id):
    db = get_db()
    request_data = request.args
    # TODO: i could probably get the info i need by passing in or keeping a client timezone
    # cookie instead of always using js on the client to format a specific date
    selected_date = parse_iso(request_data.get("selectedDate"))
    selected_booking_id = int(request_data.get("bookingID", 0))

    if not selected_date:
        print(" we cached as hell babe ")
        return render_template(
            "time-slots.html",
            selected_booking_id=selected_booking_id,
            tutor_id=tutor_id,
            time_slots=session.get("cached_time_slots"),
            dates=session.get("cached_dates"),
        )
    is_cached = str(selected_date.date()) == session.get("cached_request_date")
    print(
        f"selected {str(selected_date.date())} is not the same as {session.get('cached_request_date')}"
    )
    if is_cached:
        print(" we cached as hell babe ")
        # TODO: swap this pointless rerender with some status code that says hey don't do anything
        # just leave the page as is. or maybe some hx-header?
        return render_template(
            "time-slots.html",
            selected_booking_id=selected_booking_id,
            tutor_id=tutor_id,
            time_slots=session.get("cached_time_slots"),
            dates=session.get("cached_dates"),
        )
    dates = {
        "previous": str(selected_date.date() - timedelta(days=1)),
        "selected": str(selected_date.date()),
        "next": str(selected_date.date() + timedelta(days=1)),
    }

    query = """
SELECT b.BookingID, b.TimeSlot
FROM Bookings b
JOIN TutorAvailability ta ON ta.TutorAvailabilityID = b.TutorAvailabilityID
JOIN Tutors t ON ta.TutorID = t.TutorID
WHERE t.TutorID = ?"""
    bookings = [dict(r) for r in db.execute(query, (tutor_id,)).fetchall()]
    bookings = [
        b
        for b in bookings
        if in_display_range(selected_date, parse_iso(b.get("TimeSlot")))
    ]
    time_slots = map_bookings_to_time_slots(bookings, selected_date)
    session.update({"cached_time_slots": time_slots})
    session.update({"cached_dates": dates})
    session.update({"cached_request_date": str(selected_date.date())})

    return render_template(
        "time-slots.html",
        time_slots=time_slots,
        dates=dates,
        selected_booking_id=selected_booking_id,
        selected_date=str(selected_date.date()),
        tutor_id=tutor_id,
    )


def map_bookings_to_time_slots(bookings, selected_date):
    mapped = {
        "previous": [],
        "selected": [],
        "next": [],
    }
    for b in bookings:
        date = parse_iso(b.get("TimeSlot")).date()
        if date == selected_date.date():
            mapped["selected"].append(b)
            b.update({"TimeSlot": str(parse_iso(b.get("TimeSlot")).timetz())})
        elif date == selected_date.date() - timedelta(days=1):
            mapped["previous"].append(b)
            b.update({"TimeSlot": str(parse_iso(b.get("TimeSlot")).timetz())})
        elif date == selected_date.date() + timedelta(days=1):
            mapped["next"].append(b)
            b.update({"TimeSlot": str(parse_iso(b.get("TimeSlot")).timetz())})

    return mapped


def in_display_range(selected_date: datetime, other_date: datetime) -> bool:
    difference = abs(selected_date.date() - other_date.date())
    return difference.days <= 1


def parse_iso(iso_string) -> datetime | None:
    if not iso_string:
        return None
    if iso_string.endswith("Z"):
        iso_string = iso_string[:-1] + "+00:00"
    return datetime.fromisoformat(iso_string)


@bp.route("/<booking_id>", methods=["GET"])
def get_form(booking_id):
    db = get_db()
    query = """
SELECT b.BookingID,
    b.TimeSlot,
    t.Name AS TutorName,
    t.Email,
    t.TutorID
FROM Bookings b
    JOIN TutorAvailability ta ON b.TutorAvailabilityID = ta.TutorAvailabilityID
    JOIN Tutors t ON t.TutorID = ta.TutorID
WHERE b.BookingID = ?
"""
    booking_and_tutor = dict(db.execute(query, (booking_id,)).fetchone())
    return render_template("booking_form.html", booking=booking_and_tutor)


@bp.route("/<tutor_id>/<booking_id>/submit", methods=["POST"])
def submit_booking(tutor_id, booking_id):
    # get form values (i don't even use these rn)
    # update booking entry to booked
    db = get_db()
    query = """
UPDATE Bookings
SET IsBooked = 1
WHERE BookingID = ?
"""
    db.execute(query, (booking_id,))
    db.commit()
    flash("Booking submitted successfully!")
    response = jsonify({"location": url_for("home")})
    response.headers["HX-Redirect"] = url_for("home")

    return response


def map_py_weekday_to_utc_day(weekday: int) -> int:
    PY_TO_UTC = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 0}
    return PY_TO_UTC[weekday]


@bp.route("/<tutor_id>/create", methods=["POST"])
def generate_bookings(tutor_id):
    """accept the tutoravailability data and return 30 days worth of time slots"""

    # TODO: support override dates
    # TODO: solve the timezone bug throwing off dates in default availability ISSUE #6
    # https://blogs.oracle.com/javamagazine/post/java-timezone-part-1
    # plan: generate this based on client request which includes request date and
    # and cache unless updated by tutor
    db = get_db()
    request_time_iso = request.form.to_dict()["requestTime"]
    if request_time_iso.endswith("Z"):
        request_time_iso = request_time_iso[:-1] + "+00:00"

    request_date = datetime.fromisoformat(request_time_iso).astimezone(timezone.utc)
    if is_cached(tutor_id, request_date):
        return "cached"

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
    cache_bookings(tutor_id, request_date)

    return "success"


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


def is_cached(tutor_id, request_date: datetime):
    db = get_db()
    get_cached_query = "SELECT LastGenerated FROM BookingsCache WHERE TutorID = ?"
    found_time = db.execute(get_cached_query, (tutor_id,)).fetchone()

    if found_time:
        found_time = datetime.fromisoformat(
            dict(found_time).get("LastGenerated")
        ).astimezone(timezone.utc)
        return found_time.date() == request_date.date()


def cache_bookings(tutor_id, request_date: datetime):
    db = get_db()
    insert_query = (
        "INSERT OR REPLACE INTO BookingsCache (TutorID, LastGenerated) VALUES (?, ?)"
    )
    db.execute(insert_query, (tutor_id, request_date.isoformat()))
    db.commit()

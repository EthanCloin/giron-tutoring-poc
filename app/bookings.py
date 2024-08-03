from wsgiref.util import request_uri
from flask import (
    Blueprint,
<<<<<<< HEAD
    flash,
    jsonify,
    redirect,
    request,
    render_template,
    url_for,
=======
    request,
    render_template,
>>>>>>> 74858d3 (Add booking post and cache fxn)
)
from app.database import get_db
from datetime import datetime, timezone, timedelta


bp = Blueprint("bookings", __name__, url_prefix="/bookings")


<<<<<<< HEAD
@bp.route("/", methods=["GET"])
def get_form():
    booking_id = request.args.get("bookingID")
=======
@bp.route("/<int:booking_id>", methods=["GET"])
def submit_booking_view(booking_id):
>>>>>>> 74858d3 (Add booking post and cache fxn)
    db = get_db()
    query = """
SELECT b.BookingID,
    b.TimeSlot,
    t.Name AS TutorName,
<<<<<<< HEAD
    t.Email,
    t.TutorID
=======
    t.Email
>>>>>>> 74858d3 (Add booking post and cache fxn)
FROM Bookings b
    JOIN TutorAvailability ta ON b.TutorAvailabilityID = ta.TutorAvailabilityID
    JOIN Tutors t ON t.TutorID = ta.TutorID
WHERE b.BookingID = ?
"""
    booking_and_tutor = dict(db.execute(query, (booking_id,)).fetchone())
<<<<<<< HEAD
    print("ctx: ", booking_and_tutor)
    return render_template("booking_form.html", booking=booking_and_tutor)


@bp.route("/<tutor_id>/<booking_id>/submit", methods=["POST"])
def submit_booking(tutor_id, booking_id):
    # get form values (i don't even use these rn)
    # update booking entry to booked
    print("booking: ", booking_id)
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


=======
    return render_template("booking_form.html", booking=booking_and_tutor)


>>>>>>> 74858d3 (Add booking post and cache fxn)
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

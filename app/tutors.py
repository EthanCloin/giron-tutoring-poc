from flask import (
    Blueprint,
    render_template,
)
from app.database import get_db

bp = Blueprint("tutors", __name__, url_prefix="/tutors")


# home route should be list of tutors
# all routes in this blueprint start with '/tutors', so this "/" is really "/tutors"
@bp.route("/")
def all_tutors_view():
    db = get_db()
    query = "SELECT t.TutorID, t.Name FROM Tutors t"
    tutors = db.execute(query).fetchall()
    return render_template("tutors-list.html", tutors=tutors)


@bp.route("/<int:tutor_id>")
def tutor_detail_view(tutor_id: int):
    """
    primary tutor page. shows tutor name and description etc
    include a button to pull up availability
    """
    db = get_db()
    tutor_name = db.execute(
        "SELECT Name FROM Tutors WHERE TutorID=?", (tutor_id,)
    ).fetchone()[0]
    query = "SELECT DayUTC, TimeUTC FROM TutorAvailability WHERE TutorID=? AND OverrideDatetimeUTC IS NULL"
    availability = [dict(r) for r in db.execute(query, (tutor_id,)).fetchall()]
    days_available = set(a["DayUTC"] for a in availability)
    return render_template(
        "tutor-detail.html",
        tutor_name=tutor_name,
        tutor_id=int(tutor_id),
        availability=availability,
        days_availabile=days_available,
    )


# @bp.route("/<int:tutor_id>/availability")
# def tutor_availability_view(tutor_id: int):
#     """
#     this should return a modal that includes a calendar widget and reactive time slots for the selected
#     day, preceding day, and following day.
#     """
#     db = get_db()
#     query = "SELECT DayUTC, TimeUTC FROM TutorAvailability WHERE TutorID=? AND OverrideDatetimeUTC IS NULL"
#     availability = [dict(r) for r in db.execute(query, (tutor_id,)).fetchall()]
#     days_available = set(a["DayUTC"] for a in availability)
#     return render_template(
#         "tutor-availability.html",
#         availability=availability,
#         days_available=days_available,
#     )


@bp.route("/booking/<int:booking_id>", methods=["GET"])
def submit_booking_view(booking_id):
    db = get_db()
    query = """
SELECT b.BookingID,
    b.TimeSlot,
    t.Name AS TutorName,
    t.Email
FROM Bookings b
    JOIN TutorAvailability ta ON b.TutorAvailabilityID = ta.TutorAvailabilityID
    JOIN Tutors t ON t.TutorID = ta.TutorID
"""
    booking_and_tutor = db.execute(query, booking_id)
    return render_template("booking_form.html", booking=booking_and_tutor)

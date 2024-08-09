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
    query = """
SELECT ta.DayUTC, ta.TimeUTC, t.Name AS TutorName
FROM TutorAvailability ta 
JOIN Tutors t ON t.TutorID = ta.TutorID 
WHERE ta.TutorID=? AND ta.OverrideDatetimeUTC IS NULL
    """
    availability = [dict(r) for r in db.execute(query, (tutor_id,)).fetchall()]
    days_available = set(a["DayUTC"] for a in availability)
    tutor_name = availability[0].get("TutorName")

    ts_query = """
SELECT b.TimeSlot, b.BookingID
FROM Bookings b
JOIN TutorAvailability ta on ta.TutorAvailabilityID = b.TutorAvailabilityID
JOIN Tutors t on t.TutorID = ta.TutorID
WHERE t.TutorID = ?
  AND b.IsBooked = 0
"""
    res = db.execute(ts_query, (tutor_id,)).fetchall()
    time_slots = [dict(r) for r in res]

    return render_template(
        "tutor-detail.html",
        tutor_name=tutor_name,
        tutor_id=int(tutor_id),
        days_available=days_available,
        db_time_slots=time_slots,
    )

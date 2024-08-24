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
SELECT t.TutorID, t.Name
FROM Tutors t
WHERE t.TutorID = ?
"""
    res = db.execute(query, (tutor_id,)).fetchall()
    tutor = {"Name": res[0]["Name"], "TutorID": res[0]["TutorID"]}

    return render_template(
        "tutor-detail.html",
        tutor=tutor,
    )

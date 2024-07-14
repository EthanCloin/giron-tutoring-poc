from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.database import get_db

bp = Blueprint("tutors", __name__, url_prefix="/tutors")


@bp.route("/")
def tutor_detail_view():
    """
    primary tutor page. shows tutor name and description etc
    include a button to pull up availability
    """
    return render_template("tutor-detail.html")


@bp.route("/<tutor_id>/availability")
def tutor_availability_view(tutor_id):
    """
    this should return a modal that includes a calendar widget and reactive time slots for the selected
    day, preceding day, and following day.
    """
    return "this is availability biatch"


import datetime
import re
import itertools

from flask import Blueprint, render_template, request, redirect, url_for, session
from knoerden.lib.utils import request_data, abort
from knoerden.lib import database

blueprint = Blueprint("meetings", __name__, url_prefix="/meetings/")

@blueprint.route("/")
def list():
    meetings = database.execute("select * from meetings order by date asc")
    meetings_by_year = itertools.groupby(meetings, key=lambda meeting: meeting.date.year)
    return render_template("meetings.html", meetings_by_year=meetings_by_year)


@blueprint.route("meeting/<int:meeting_id>/", methods=["GET", "POST"])
def meeting(meeting_id):
    if request.method == "POST":
        data = request_data()
        data.x
        if data.is_attending == "yes":
            is_attending = True
        elif data.is_attending == "no":
            is_attending = False
        else:
            raise Exception("Unknown input for is_attending {}".format(data.is_attending))

        with database.transaction() as transaction:
            transaction.execute("delete from meetings_users where meeting_id = ? and user_id = ?", meeting_id, session["user_id"])
            transaction.create("meetings_users", meeting_id=meeting_id, user_id=session["user_id"], is_attending=data.is_attending, note=data.note)
        # database.execute("insert into meetings_users (meeting_id, user_id, is_attending, note) values (?, ?, ?, ?) on conflict do update set is_attending = ?, note = ?, updated_at = ? ", meeting_id, session["user_id"], data.is_attending, data.note, data.is_attending, data.note, datetime.datetime.utcnow())
    meeting = database.execute("select * from meetings where meeting_id = ?", meeting_id).one()
    users = database.execute("select * from meetings_users inner join users using (user_id) where meeting_id = ?", meeting_id)
    number_of_attending = sum(1 for x in users if x.is_attending)
    return render_template("meeting.html", meeting=meeting, users=users, number_of_attending=number_of_attending)


@blueprint.route("add/", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("meetings_add.html")
    if request.method == "POST":
        data = request_data()
        date = datetime.datetime.strptime(data.date, "%Y-%m-%d") # eg: Tue, 22 Nov 2011 06:00:00 GMT"
        time_parts = re.split(" *[.,:;] *", data.time.strip())
        if len(time_parts) == 1:
            hour = time_parts[0]
            minute = 0
        elif len(time_parts) == 2:
            hour = time_parts[0]
            minute = time_parts[1]
        else:
            abort(f"Invalid time format: {data.time}")
        try:
            date = date.replace(hour=int(hour), minute=int(minute))
        except Exception:
            abort(f"Invalid time format: {data.time}")
        meeting = database.create("Meetings",
                                  date=date,
                                  title=data.title,
                                  description=data.description,
                                  created_by=session["user_id"])
        return redirect(url_for("meetings.list"))

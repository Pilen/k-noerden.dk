
from flask import session
from knoerden.lib import database

_all_filters = {}
def filter(func):
    _all_filters[func.__name__] = func
    return func

def init_filters(app):
    for name, filter in _all_filters.items():
        app.jinja_env.filters[name] = filter


@filter
def month(datetime):
    months = ["Januar",
              "Februar",
              "Marts",
              "April",
              "Maj",
              "Juni",
              "Juli",
              "August",
              "September",
              "Oktober",
              "November",
              "December"]
    return months[datetime.month-1]

@filter
def weekday(datetime):
    weekdays = ["Mandag",
                "Tirsdag",
                "Onsdag",
                "Torsdag",
                "Fredag",
                "Lørdag",
                "Søndag"]
    return weekdays[datetime.weekday()]

@filter
def date(datetime):
    return f"{weekday(datetime)} {datetime.day}. {month(datetime)} {datetime.hour:02d}:{datetime.minute:02d}"

@filter
def user(user):
    is_me = "user_id" in session and session["user_id"] == user.user_id
    return f"{user.username}" + ("!" if is_me else "")

@filter
def fetch_user(user_id):
    print (user_id)
    user_ = database.execute("select * from users where user_id = ?", user_id).one()
    return user(user_)

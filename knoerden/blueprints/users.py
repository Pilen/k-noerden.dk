
from flask import Blueprint, render_template, request, redirect, url_for
from knoerden.lib import database, config
from knoerden.lib.user import password_check, authenticate, unauthenticate
from knoerden.lib.utils import request_data, abort

blueprint = Blueprint("users", __name__, url_prefix="/users/")

@blueprint.route("login/", methods=["POST"])
def login():
    data = request_data()
    print(data)
    users = database.execute("select user_id, username, password, is_deleted from Users inner join Passwords using (user_id) where lower(username) = ?", data.username.lower())
    print(users)
    user = users.one(error="Invalid username")
    if user.is_deleted:
        abort("User is deleted")
    if not password_check(data.password, user.password):
        abort("Invalid password")
    authenticate(user)
    return redirect(request.referrer)

@blueprint.route("logout/")
def logout():
    unauthenticate()
    return redirect(url_for("frontpage.frontpage"))

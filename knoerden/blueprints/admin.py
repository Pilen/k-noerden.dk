
# from flask import Blueprint, render_template, request, redirect
# from lib import database, config
# from lib.utils import logged_in, success
# blueprint = Blueprint("admin", __name__, url_prefix="/admin/")

# @blueprint.route("api/invite", methods=["POST"])
# @logged_in("admin")
# def invite():
#     data = request_data()
#     while True:
#         with database.transaction():
#             database.execute("delete from user_invitation_keys where email = ?", data.email)
#             key = secrets.token_urlsafe(config.INVITATION_KEY_LENGTH)
#             existing = database.execute("select key from user_invitation_keys where key = ?", key)
#             if len(existing) != 0:
#                 continue
#             try:
#                 database.create("user_invitation_keys", key=key, email=data.email)
#             except psycopg2.IntegrityError as e:
#                 continue
#         url = config.URL + "/user/new?key=" + key
#         mail.invitation.format(url=url).send(data.email)
#         return success()

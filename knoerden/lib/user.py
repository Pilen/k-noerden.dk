
import bcrypt
import base64
import hashlib
import string

from flask import session

from knoerden.lib import database, config
from knoerden.lib.utils import abort

def password_prehash(raw_password):
    return base64.b64encode(hashlib.sha256(raw_password.encode("utf-8")).digest())

def password_hash(raw_password):
    salt = bcrypt.gensalt(config.BCRYPT_ROUNDS)
    # To handle passwords longer than the supported 72 chars of bcrypt
    prehashed = password_prehash(raw_password)
    return bcrypt.hashpw(prehashed, salt).decode("utf-8")

def password_check(raw_password, hashed_password):
    """Return True if raw_password hashes to enc_password else False"""
    prehashed = password_prehash(raw_password)
    return bcrypt.checkpw(prehashed, hashed_password.encode("utf-8"))

def create_user(username, name, password, email):
    """Create a new user with given username, password and email"""
    with database.transaction():
        existing = database.execute("select user_id from Users where lower(username) = ?", username.lower())
        if len(existing) > 0:
            abort(f"Username '{username}' already taken")
        user = database.create("users", username=username, name=name, email=email)
        hashed = password_hash(password)
        database.create("Passwords", user_id=user.user_id, password=hashed)
        return user

def valid_username(username):
    alphabet = set(string.ascii_letters + "æøåÆØÅ")
    legal_characters = alphabet.union("-_0123456789")

    return (len(username) >= 0 and # username must not be empty
            all(c in legal_characters for c in username) and
            any(c in alphabet for c in username))

def valid_password(password):
    return len(password) >= config.PASSWORD_MIN_LENGTH


def update_password(user_id, raw_password):
    password = hash(raw_password)
    database.execute("update Passwords set password = ? where user_id = ?", password, user_id)

def add_user_to_group(user_id, group):
    with data.transaction():
        group_id = data.execute("select group_id from Groups where groupname = ?", group)
        database.create("Users_groups", user_id=user_id, group_id=group_id)

def remove_user_from_group(user_id, group):
    with data.transaction():
        group_id = data.execute("select group_id from Groups where groupname = ?", group)
        database.execute("delete from Users_groups where user_id = ? and group_id = ?", group_id)

def authenticate(user):
    session["user_id"] = user.user_id
    session["username"] = user.username
    all_groups = database.execute("select groupname from groups").scalars()
    groups = database.execute("select groupname from groups inner join users_groups using (group_id) where user_id = ?", user.user_id).scalars()
    group_dict = {group: False for group in all_groups}
    for group in groups:
        group_dict[group] = True
    session["groups"] = group_dict

def unauthenticate():
    session.clear()

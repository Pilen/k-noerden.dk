
from flask import request
from flask.json import jsonify

class Attributable:
    def __init__(self, data):
        self._data = data

    def __getattr__(self, key):
        if key in self._data:
            return self._data[key]
        else:
            raise AttributeError(f"{key} is missing in the request")

    def __repr__(self):
        return "Attributable({})".format(repr(self._data))

    def get_or_fail(self, key, code=None, message=None):
        if key not in self:
            return abort(code, message)
        return self[key]


def request_data():
    result = dict()
    result.update(request.args)
    result.update(request.form)
    if request.is_json:
        result.update(request.get_json())
    return Attributable({key: value[0] for key, value in result.items()})


def logged_in(*groups):
    def decorator(fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            if ("user_id" in session and
                (len(args) == 0 or # Anyone logged in can access
                 any(session["groups"].get(group, False) for group in groups) or # User is in allowed group
                 session["groups"].get("admin", False))):  # User is admin
                return fn(*args, **kwargs)
            else:
                abort(403)
        return decorated
    return decorator


def success(message=None):
    result = dict(success=True)
    if message is not None:
        result["message"] = message
    return jsonify(result)


class AbortException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


def abort(code=None, message=None):
    if code is None:
        code == 400
    if message is None and not isinstance(code, int):
        message = code
        code = 400
    raise AbortException(code, message)

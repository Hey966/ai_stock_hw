from functools import wraps
from flask import request, Response

USERNAME = "966"
PASSWORD = "123456"


def check_auth(username, password):
    return username == USERNAME and password == PASSWORD


def authenticate():
    return Response(
        "需要登入",
        401,
        {"WWW-Authenticate": 'Basic realm="AI Stock Login"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
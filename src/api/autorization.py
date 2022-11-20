import datetime
import json
import jwt

from flask import Response, request, session

from src.api import app
from src.api.roles import NonRegistered, Registered
from src.db.helpers import get_user_info, login_by_email_helper
from src.redis.init_db import r


class AuthenticationError(BaseException):
    def __init__(self, message) -> None:
        super().__init__(message)


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload["sub"]
    except jwt.InvalidTokenError as e:
        raise Exception("Invalid token. Please log in again.") from e


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    except Exception as e:
        return e


def autorize(email, password):
    user = login_by_email_helper(email)

    if password == user.get("password"):
        return encode_auth_token(user.get("username"))

    return f"Password is incorrect"


def autorize_to_system():
    return autorize(email=request.form["username"], password=request.form["password"])


def create_user_builder():
    try:

        username = decode_auth_token(session["token"])

    except Exception:
        return NonRegistered()

    return Registered(username)

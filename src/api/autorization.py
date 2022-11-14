import datetime
import json
import jwt

from flask import request

from src.api import app
from src.api.permissions import is_user_is_admin
from src.api.roles import NonRegistered, Registered
from src.db.helpers import get_user_info, login_by_email_helper
from src.redis.init_db import r


class AuthenticationError(Exception):
    pass

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
    try:

        user = login_by_email_helper(email)

    except Exception as e:
        return f"Something going wrong. {e}"

    if password == user.get("password"):
        return encode_auth_token(user.get("username"))

    return f"Password is incorrect"


def autorize_to_system():
    try:

        email = request.form["username"]

    except Exception as e:
        raise AuthenticationError from e

    else:

        password = request.form["password"]

        if password == "":
            raise AuthenticationError("Please input your password")

        else:
            return autorize(email, password)


def create_user_builder():
    head = request.headers.environ
    token = str(head.get("HTTP_AUTHORIZATION")).split(" ")[-1]

    try:

        username = decode_auth_token(token)

    except Exception:
        return NonRegistered()

    return Registered(username)

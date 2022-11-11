from datetime import datetime
import json

from src.api import app
from src.db.helpers import create_user_db
from src.redis.init_db import r

from flask import request


def _get_email():
    try:

        email = request.authorization.get("username")

    except Exception:
        return {"msg": "Please input your email for registration", "status": False}
    else:
        if (email or email.split("@")[0]) == "":
            return {
                "msg": "Please input a valid email. Example: 'user@m.com' or 'user'",
                "status": False,
            }

    return {
        "msg": email if "@m.com" in email else email.join("@m.com"),
        "status": True,
    }


def _get_password():
    password = request.authorization.get("password")

    if password == "":
        return {"msg": "Please input password", "status": False}

    return {"msg": password, "status": True}


@app.route("/create", methods=["POST"])
def create_user():
    email = _get_email()
    if not email.get("status"):
        return email.get("msg")

    password = _get_password()
    if not password.get("status"):
        return password.get("msg")

    username = email.get("msg").split("@")[0]
    # user_id = _generate_username(name)
    return create_user_db(
        {
            "email": email.get("msg"),
            "username": username,
            "password": password.get("msg"),
            "favorite": "Do not declarated",
            "admin_role": 0,
        }
    )

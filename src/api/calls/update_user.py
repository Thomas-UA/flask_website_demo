import json

from src.api import app
from src.api.autorization import create_user_builder, decode_auth_token
from src.api.calls.get_user import get_my_profile
from src.api.roles import NonRegistered, Registered
from src.db.helpers import get_user_info, update_user_db
from src.redis.init_db import r

from flask import redirect, render_template, request, session


def _set_new_data():
    return_dict = {}
    return_dict["password"] = f"{request.form['password']}" if f"{request.form['password']}" != "" else None
    return_dict["favorite"] = f"{request.form['favorite']}" if f"{request.form['favorite']}" != "" else None

    return return_dict


@app.route("/profile", methods=["GET", "POST"])
def update_user():
    if request.method == "GET": 
        return get_my_profile()

    username = decode_auth_token(session["token"])
    new_data = _set_new_data()

    update_user_db(
        username=username,
        new_data=new_data
    )

    return get_my_profile()

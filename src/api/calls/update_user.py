import json

from src.api import app
from src.api.autorization import create_user_builder
from src.api.roles import NonRegistered, Registered
from src.db.helpers import update_user_db
from src.redis.init_db import r

from flask import request


def _set_new_data():
    return_dict = {}
    return_dict["email"] = f"{request.args['email']}"
    return_dict["password"] = f"{request.args['password']}"
    return_dict["username"] = f"{request.args['username']}"
    return_dict["favorite"] = f"{request.args['favorite']}"

    return return_dict


@app.route("/update_user/<string:user_name>", methods=["PATCH"])
def update_user(user_name):
    user_session = create_user_builder()
    if type(user_session) is not Registered:
        return f"Please login to change data"

    if user_session.is_user_owner(user_name):
        return f"You can't change other users data"

    new_data = _set_new_data()
    return update_user_db(user_name, new_data)

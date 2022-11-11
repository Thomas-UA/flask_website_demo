from collections import OrderedDict
import json

from src.api import app
from src.api.autorization import create_user_builder
from src.api.roles import Registered
from src.api.permissions import is_user_owner

from src.db.helpers import get_all_user_info, get_user_info

from src.redis.init_db import r

from flask import request


def _get_users(fields):
    user_info = get_all_user_info(fields)
    return user_info


def _get_user(user_id, fields):
    user_info = get_user_info(user_id, fields)
    if not user_info:
        return f"User {user_id} not found"
    return OrderedDict(user_info)


def _get_fields_by_permission(query_user):
    user_session = create_user_builder()
    fields = user_session.list_of_fields
    if query_user and type(user_session) is Registered:
        fields = user_session.is_user_owner(query_user)

    return fields


@app.route("/users", methods=["GET"])
def get_all_users():
    fields = _get_fields_by_permission(None)

    all_users = _get_users(fields)
    return_dict = {}
    for user in all_users:
        return_dict[user.pop("username")] = user
    return return_dict, 200


@app.route("/user/<string:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    if not user_id:
        return "You should add an Id for this operation"

    fields = _get_fields_by_permission(user_id)

    return _get_user(user_id, fields), 200

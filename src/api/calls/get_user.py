import json

from src.api import app
from src.api.autorization import create_user_builder
from src.api.roles import UserOwner

from src.redis.init_db import r

from flask import request


def _id_in_request():
    if 'id' in request.args:
        return f"{request.args['id']}"

    return False


def _is_user_owner(key, email):
    try:

        return email == json.loads(r.get(key)).get('email')

    except Exception:
        return False

def _get_users(fields):
    all_keys = r.keys()
    if not fields:
        for key in all_keys:
            yield {key: json.loads(r.get(key))}
    
    else:
        limited_dict = {}
        for key in all_keys:
            limited_dict[key] = {}
            for field in fields:
                limited_dict[key][field] = json.loads(r.get(key)).get(field)

            yield limited_dict
            limited_dict = {}

def _get_user(id, fields):    
    try:

        data = json.loads(r.get(id))

    except Exception:
        return f'User with id: {id} are not found'
    else:
        if not fields:
            return data

        limited_dict = {}
        limited_dict[id] = {}
        for field in fields:
            limited_dict[id][field] = json.loads(r.get(id)).get(field)

        return limited_dict

def _get_fields_by_permission(id=None):
    user_session = create_user_builder()
    if type(user_session) == str:
        # return message
        message = user_session
        return message

    if _is_user_owner(id, user_session.email):
        user_session = UserOwner()

    return user_session.list_of_fields


@app.route('/users', methods=['GET'])
def get_all_users():
    fields = _get_fields_by_permission()
    if type(fields) == str:
        return fields

    return list(_get_users(fields))[::-1]

@app.route('/user', methods=['GET'])
def get_user_by_id():
    id = _id_in_request()
    if not id:
        return 'You should add an Id for this operation'

    fields = _get_fields_by_permission(id)
    if type(fields) == str:
        return fields

    return _get_user(id, fields)

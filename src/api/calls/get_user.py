from collections import OrderedDict
import json

from src.api import app
from src.api.autorization import create_user_builder
from src.api.roles import UserOwner
from src.api.permissions import is_user_owner

from src.db import get_all_user_info, get_user_info

from src.redis.init_db import r

from flask import request


def _get_users(fields):
    all_keys = r.keys()
    if not fields:
        for key in all_keys:
            yield {key: json.loads(r.get(key))}
    
    else:
        limited_dict = {}
        for key in all_keys:
            limited_dict[key] = {}
            data = json.loads(r.get(key))
            for field in fields:
                limited_dict[key][field] = data.get(field)

            yield limited_dict
            limited_dict = {}

def _get_user(user_id): #, fields):
    return get_user_info(user_id)
    '''
    try:

        data = json.loads(r.get(user_id))

    except Exception:
        return f'User with id: {user_id} are not found'
    else:
        if not fields:
            return data

        limited_dict = {}
        limited_dict[user_id] = {}
        for field in fields:
            limited_dict[user_id][field] = data.get(field)

        return limited_dict
    '''

def _get_fields_by_permission(user_id=None):
    user_session = create_user_builder()
    if type(user_session) == str:
        # returning message
        return user_session

    try:

        is_user_is_owner = is_user_owner(user_id, user_session.email)
    
    except Exception:
        pass
    else:
        if is_user_is_owner:
            user_session = UserOwner()

    return user_session.list_of_fields


@app.route('/users', methods=['GET'])
def get_all_users():
    """
    fields = _get_fields_by_permission()
    if type(fields) == str:
        return fields
    """
    all_users = get_all_user_info()
    return_dict = {}
    for user in all_users:
        return_dict[user.pop('username')] = user
    return OrderedDict(return_dict)

@app.route('/user/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    if not user_id:
        return 'You should add an Id for this operation'
    '''
    fields = _get_fields_by_permission(user_id)
    if type(fields) == str:
        # returning error message
        return fields
    '''
    return _get_user(user_id), 200

import json
from api.roles import Admin, NonRegistered, Registered, UserOwner

from src.redis.init_db import r

from flask import request


def _is_user_owner(key, username):
    return username == json.loads(r.get(key).get('username'))

def autorize(username, password):
    all_keys = r.keys()
    for key in all_keys:
        username_db = json.loads(r.get(key)).get('username')
        password_db = json.loads(r.get(key)).get('password')
        if username == username_db:      
            if password == password_db:
                return {
                    'msg': key,
                    'status': False
                }

            else:
                return {
                    'msg': 'Forgot your password, call to super admin B)',
                    'status': False
                }

    return {
        'msg': 'Your nickname are not stored in db. Create an acount',
        'status': False
    }

def autorize_to_system():
    try:

        username = request.authorization['username']

    except Exception:
        return {'msg': 'Please input username in field', 'status': True}

    else:
        try:
            
            password = request.authorization['password']

        except Exception:
            return {'msg': 'Please type your password', 'status': False}

        else:
            return autorize(username, password)

def create_user_builder():
    # if users succesfully logged message get key
    message, status = autorize_to_system()
    if not status:
        return message
    
    key = message

    if json.loads(r.get(key)).get('admin_role', False):
        user = Admin()

    else:
        try:

            username = request.authorization['username']

        except Exception:
            user = NonRegistered()

        if _is_user_owner(key, username):
            user = UserOwner()
            
        user = Registered()

    return user

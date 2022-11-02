import json
from src.api.roles import Admin, NonRegistered, Registered, UserOwner

from src.redis.init_db import r

from flask import request


def _is_user_is_admin(key):
    return json.loads(r.get(key)).get('admin_role', False)

def autorize(email, password):
    all_keys = r.keys()
    for key in all_keys:
        email_db = json.loads(r.get(key)).get('email')
        password_db = json.loads(r.get(key)).get('password')
        if email == email_db:      
            if password == password_db:
                return {
                    'msg': key,
                    'email': email,
                    'status': True
                }

            else:
                return {
                    'msg': 'Forgot your password?, call to super admin B)',
                    'status': False
                }

    return {
        'msg': 'Your nickname are not stored in db. Create an acount',
        'status': False
    }

def autorize_to_system():
    try:

        email = request.authorization['username']

    except Exception:
        return {
            'msg': None,
            #'Please input email in field'
            'status': True
        }

    else:
            
        password = request.authorization['password']

        if password == '':
            return {'msg': 'Please type your password', 'status': False}

        else:
            return autorize(email, password)

def create_user_builder():
    ats = autorize_to_system()
    message, status = ats.get('msg'), ats.get('status')
    if not message:
        return NonRegistered()

    elif not status:
        return message

    # if users succesfully logged message get key
    key = message

    if _is_user_is_admin(key):
        return Admin()

    user = Registered()
    user.email = ats.get('email')
    return user

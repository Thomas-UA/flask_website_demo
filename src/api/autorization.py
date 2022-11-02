import json

from src.redis.init_db import r

from flask import request

def autorize(username, password):
    all_keys = r.keys()
    for key in all_keys:
        username_db = json.loads(r.get(key)).get('username')
        password_db = json.loads(r.get(key)).get('password')
        if username == username_db:      
            if password == password_db:
                return key

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
        return {'msg': 'Please input username in field', 'status': False}

    else:
        try:
            
            password = request.authorization['password']

        except Exception:
            return {'msg': 'Please type your password', 'status': False}
        else:
            return autorize(username, password)

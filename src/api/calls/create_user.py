from datetime import datetime
import json

from src.api import app
from src.redis.init_db import r

from flask import request


DICT_EXAMPLE = {}

def _generate_uniq_username(all_keys, user_name, count=1):
    if user_name not in all_keys:
        return user_name

    user_id = user_name.join(str(count))
    if user_id in all_keys:
        _generate_uniq_username(all_keys, user_id, count+1)

    return user_id

def _generate_username(name: str):
    all_keys = r.keys()
    user_id = "".join(c for c in name.lower() if c.isalnum())
    return _generate_uniq_username(all_keys, user_id)

def _is_user_in_database(email):
    keys = r.keys()
    emails = []
    for key in keys:
        emails.append(json.loads(r.get(key)).get('email'))

    if email in emails:
        return True

    return False

def _get_email():
    try:

        email = request.authorization.get('username')

    except Exception:
        return False
    else:
        if (email or email.split('@')[0]) == '':
            return False

    return email if '@m.com' in email else email.join('@m.com')

def _get_password():
    password = request.authorization.get('password')

    if password == '':
        return False
    
    return password


@app.route('/create', methods=['POST'])
def create_user():
    email = _get_email()
    if not email:
        return 'If you want create user please input valid email and password in the registration form'

    if _is_user_in_database(email):
        return 'User already registered, call to super admin if you forgot your password B)'

    password = _get_password()
    if not password:
        return 'Please input password in the registration form'

    name = email.split('@')[0]
    user_id = _generate_username(name)
    r.set(
        name=user_id,
        value=json.dumps(
            {
                "email": email,
                "password": password,
                "name": name,
                "registration_date": str(datetime.now()),
                "admin_role": False,
                "favorite": "Do not declarated"
            }
        ),
        # ex=360
    )

    return f'User created. Id: {user_id}. Data: {r.get(user_id)}'

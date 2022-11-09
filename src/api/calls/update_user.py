import json

from src.api import app
from src.api.autorization import create_user_builder
from src.api.permissions import is_user_owner
from src.api.roles import Admin, NonRegistered
from src.db import update_user_db
from src.redis.init_db import r

from flask import request


def _set_new_data():
    return_dict = {}
    try:

        email = f"{request.args['email']}"
        return_dict['email'] = email

    except Exception:
            pass

    try:
            
        password = f"{request.args['password']}"
        return_dict['password'] = password
        
    except Exception:
        pass

    try:

        name = f"{request.args['name']}"
        return_dict['name'] = name

    except Exception:
        pass
        
    try:
            
        favorite = f"{request.args['favorite']}"
        return_dict['favorite'] = favorite

    except Exception:
        pass

    return return_dict


@app.route('/update_user/<string:user_name>', methods=['PATCH'])
def update_user(user_name):
    if user_name == 'super_admin':
        return 'SUPER ADMIN CANNOT BE UPDATED'
    
    new_data = _set_new_data()

    return update_user_db(user_name, new_data)

"""
    user_session = create_user_builder()
    if type(user_session) == str:
        # returning message
        return user_session

    try:

        is_user_is_owner = is_user_owner(user_name, user_session.email)

    except Exception:
        if type(user_session) is NonRegistered:
            return "Please login to sustem to update user account"

    is_user_admin = True if type(user_session) is Admin else False

    if is_user_admin or is_user_is_owner:
        current_value = json.loads(r.get(user_name))

        email, password, name, favorite, registration_date = \
            current_value.get('email', None),\
            current_value.get('password', None),\
            current_value.get('name', None),\
            current_value.get('favorite', None),\
            current_value.get('registration_date')

        new_data = _set_new_data(is_user_admin)

        try:
            
            r.set(
                name=user_name,
                value=json.dumps(
                    {
                        'email': new_data.get('email', email),
                        'password': new_data.get('password', password),
                        'name': new_data.get('name', name),
                        'favorite': new_data.get('favorite', favorite),
                        'admin_role': new_data.get('admin_role', None),
                        'registration_date': registration_date
                    }
                )
            )

        except Exception:
            return 'Something goig wrong'
        else:
            return f'User: {user_name} succefully updated. New values: {r.get(user_name)}'

    return "You don't have persmission to update other users account"
"""
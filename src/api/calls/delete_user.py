from src.api import app
from src.api.autorization import create_user_builder
from src.api.permissions import is_user_owner
from src.api.roles import Admin, NonRegistered
from src.redis.init_db import r


@app.route('/delete_user/<string:user_name>', methods=['DELETE'])
def delete_user(user_name):
    if user_name == 'super_admin':
        return 'SUPER ADMIN CANNOT BE DELETED'

    user_session = create_user_builder()
    if type(user_session) == str:
        # returning message
        return user_session

    try:

        is_user_is_owner = is_user_owner(user_name, user_session.email)

    except Exception:
        if type(user_session) is NonRegistered:
            return "Please login to system to delete user account"

    is_user_admin = True if type(user_session) is Admin else False

    if is_user_admin or is_user_is_owner:
        try:
            
            r.delete(user_name)
        
        except Exception:
            return 'Something goig wrong'
        else:
            return f'User: {user_name} succefully deleted'

    return "You don't have persmission to delete other users account"

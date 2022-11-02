import json

from src.api import app
from src.redis.init_db import r

from flask import request


def _id_in_request():
    if 'id' in request.args:
        return f"{request.args['id']}"

    return False

def _get_users():
    all_keys = r.keys()
    for key in all_keys:
        yield {key: json.loads(r.get(key))}
    
def _get_user(id):    
    try:
            
        return json.loads(r.get(id))
        
    except Exception:
        return f'User with id: {id} are not found'

def _get_info_by_permission():
    pass


@app.route('/users', methods=['GET'])
def get_all_users():
    return list(_get_users())[::-1]


@app.route('/user', methods=['GET'])
def get_user_by_id():
    id = _id_in_request()
    if not id:
        return 'You should add an Id for this operation'

    return _get_user(id)

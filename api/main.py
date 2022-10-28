from redis_db.main import r

from flask import Flask, request

app = Flask(__name__)


@app.errorhandler(500)
def internal_error(error):
    return '''500 error'''

@app.errorhandler(400)
def internal_error(error):
    return '''400 error'''



@app.route('/hw', methods=['GET'])
def get_hello_world():
    return '''Hello world'''

@app.route('/users', methods=['GET'])
def get_all_users():
    return None

@app.route('/user/', methods=['GET'])
def get_user():
    if 'id' not in request.args:
        return '''you should add id key to your request'''
    
    id = f"{request.args['id']}"
    return_value = r.get(id)

    if return_value:
        return return_value

    else:
        return f"""There no data for user with an {id} id"""

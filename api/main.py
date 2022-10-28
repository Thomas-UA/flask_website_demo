import json

from redis_db.main import r

from datetime import datetime
from flask import Flask, request

app = Flask(__name__)


@app.errorhandler(500)
def internal_error(error):
    return """500 error"""

@app.errorhandler(400)
def internal_error(error):
    return """400 error"""



@app.route("/hw", methods=["GET"])
def get_hello_world():
    return """Hello world"""

@app.route("/users", methods=["GET"])
def get_all_users():
    keys_list = r.keys()
    return_dict = {}
    for key in keys_list:
        return_dict[key] = json.loads(r.get(key))
    return return_dict

@app.route("/user", methods=["GET", "POST", "PATCH"])
def user():
    if "id" not in request.args:
        return """you should add id key to your request"""

    id = f"{request.args['id']}"

    if request.method == "POST":
        value = request.get_json()
        r.set(
            name=id,
            value=json.dumps(
                {
                    "email": value.get("email", None),
                    "password": value.get("password", None),
                    "name": value.get("name", None),
                    "registration_date": str(datetime.now())
                }
            ),
            ex=360 if (
                value["email"]
                and value["password"]
                and value["name"]
            )else 36
        )
        return_value = r.get(id)

        if return_value:
            return return_value

    elif request.method == "PATCH":
        current_value = json.loads(r.get(id))

        email, password, name = current_value['email'], current_value['password'], current_value['name']
        
        try:

            email = f"{request.args['email']}"

        except Exception:
            pass

        try:
            
            password = f"{request.args['password']}"
        
        except Exception:
            pass

        try:

            name = f"{request.args['name']}"

        except Exception:
            pass

        r.set(
            name=id,
            value=json.dumps(
                {
                    "email": email,
                    "password": password,
                    "name": name,
                    "registration_date": current_value["registration_date"]
                }
            )
        )
        return_value = r.get(id)
        if return_value:
            return return_value

    elif request.method == "GET":
        return_value = r.get(id)

        if return_value:
            return return_value

    return '''key doesn't exists'''

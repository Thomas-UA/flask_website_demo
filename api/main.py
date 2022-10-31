import json

from redis_db.main import r

from datetime import datetime
from flask import Flask, request, g
from requests.auth import HTTPDigestAuth


app = Flask(__name__)

# key is id
keys_list = r.keys()
emails_dict = {}
for key in keys_list:
    emails_dict[key] = json.loads(r.get(key)).get("email")

@app.errorhandler(500)
def internal_error_code_V(error):
    return """500 error"""

@app.errorhandler(400)
def internal_error_code_IV(error):
    return """400 error"""


def _is_user_in_db(email):
    if email not in emails_dict.values():
        keys_list = r.keys()
        for key in keys_list:
            if key not in emails_dict.keys():
                new_email = json.loads(r.get(key)).get("email")
                emails_dict[key] = new_email

                if new_email == email:
                    return True

        else:
            return False

    return True

def _get_id_by_email(email):
    k = None
    if _is_user_in_db(email):
        for key in keys_list:
            if emails_dict[key] == email:
                k = key
                break

    return k

def _is_user_registered(email):
    if email in emails_dict.values():
        return True
    
    return _is_user_in_db(email)

def _is_user_is_admin(email):
    if not _is_user_registered(email):
        return False

    key = _get_id_by_email(email)

    try:

        return json.loads(r.get(key)).get("admin_role")

    except Exception:
        return False

def autorization_to_servise(email):
    key = _get_id_by_email(email)
    if key == None:
        return {"msg": "User not found", "status": False}
    
    try:

        password = request.authorization['password']
    
    except Exception:
        return {"msg": "Something going wrong", "status": False}

    if  password != dict(json.loads(r.get(key))).get("password"):
        return {"msg": "Password is incorrect", "status": False}

    else:
        return {"msg": "Loggin successful", "status": True} 

@app.route("/hw", methods=["GET"])
def get_hello_world():
    return """Hello world"""

@app.route("/users", methods=["GET"])
def get_all_users():
    keys_list = r.keys()
    return_dict = {}
    role_attrs = ['name']
    try:
    
        email = request.authorization['username']

    except Exception:
        email = None

    message, status = autorization_to_servise(email).values()
    if status:
        if _is_user_is_admin(email):
            role_attrs = dict(json.loads(r.get('0'))).keys()

        else:
            keys_list.remove('0')
            role_attrs = ['email', 'name', 'favorite']

    else:
        return_dict["message"] = message

    for key in keys_list:
        temp_dict = dict(json.loads(r.get(key)))
        return_dict[key] = {}
        for atr in role_attrs:
            return_dict[key][atr] = temp_dict[atr]

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
                    "favorite": value.get("favorite", None),
                    "registration_date": str(datetime.now())
                }
            ),
            ex=360 if (
                value["email"]
                and value["password"]
                and value["name"]
                and value["favorite"]
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
        user_value = r.get(id)

        return_dict= {}
        role_attrs = ['name']
        if _is_user_is_admin('email'):
            role_attrs = dict(json.loads(r.get('0'))).keys()

        temp_dict = dict(json.loads(user_value))
        return_dict = {}
        for atr in role_attrs:
            return_dict[atr] = temp_dict[atr]

            return return_dict

    return """key doesn't exists"""

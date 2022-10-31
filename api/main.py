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
    _return_dict = {}
    _role_attrs = ['name']
    try:
    
        email = request.authorization['username']

    except Exception:
        email = None
    else:
        is_user_is_admin = _is_user_is_admin(email)

    message, status = autorization_to_servise(email).values()
    if status:
        if is_user_is_admin:
            _role_attrs = dict(json.loads(r.get('0'))).keys()

        else:
            keys_list.remove('0')
            _role_attrs = ['email', 'name', 'favorite']
    else:
        keys_list.remove('0')
        _return_dict["message"] = message

    for key in keys_list:
        _temp_dict = dict(json.loads(r.get(key)))
        _return_dict[key] = {}
        for _atr in _role_attrs:
            _return_dict[key][_atr] = _temp_dict[_atr]

    return _return_dict

@app.route("/user", methods=["POST", "PATCH", "GET", "DELETE"])
def user():
    if "id" not in request.args:
        return """you should add id key to your request"""

    id = f"{request.args['id']}"

    if request.method == "POST":
        value = request.get_json()
        if _is_user_registered(value.get("email")):
            return """User already registered"""

        try:
            
            log_email = request.authorization['username']

        except Exception:
            admin_role = False
            
        else:
            message, status = autorization_to_servise(log_email).values()
            if status and _is_user_is_admin(log_email):
                try:
                
                    admin_role = True if f"{value['admin_role']}".lower() == "true" else False
            
                except Exception:
                    admin_role = False
            
            else:
                admin_role = False

        r.set(
            name=id,
            value=json.dumps(
                {
                    "email": value.get("email", None),
                    "password": value.get("password", None),
                    "name": value.get("name", None),
                    "favorite": value.get("favorite", None),
                    "admin_role": admin_role,
                    "registration_date": str(datetime.now())
                }
            ),
            # ex=360 if (
            #     value["email"]
            #     and value["password"]
            #     and value["name"]
            #     and value["favorite"]
            # )else 36
        )
        return_value = r.get(id)

        if return_value:
            return return_value

    elif request.method == "PATCH":
        try:
            
            current_value = json.loads(r.get(id))

        except Exception:
            return f"""User with id: {id} are not found"""

        try:
            
            log_email = request.authorization['username']
        
        except Exception:
            return """You should log in to the system"""

        else:
            message, status = autorization_to_servise(log_email).values()
        
        if status == False:
            return message

        if log_email != current_value['email'] and not _is_user_is_admin(log_email):
            return f"""You can't chose the other user data's. The next id is your: {_get_id_by_email(log_email)}"""

        email, password, name, favorite = \
            current_value.get('email', None),\
            current_value.get('password', None),\
            current_value.get('name', None),\
            current_value.get('favorite', None)

        if _is_user_is_admin(log_email):
            try:
                
                admin_role = True if f"{request.args['admin_role']}".lower() == "true" else False
            
            except Exception:
                admin_role = False
        
        else:
            admin_role = False

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
        
        try:
            
            favorite = f"{request.args['favorite']}"

        except Exception:
            pass

        r.set(
            name=id,
            value=json.dumps(
                {
                    "email": email,
                    "password": password,
                    "name": name,
                    "favorite": favorite,
                    "admin_role": admin_role,
                    "registration_date": current_value["registration_date"]
                }
            )
        )
        return_value = r.get(id)
        if return_value:
            return return_value

    elif request.method == "GET":
        user_value = r.get(id)
        
        if not user_value:
            return f"""User with id: {id} are not found"""

        _return_dict = {}


        _role_attrs = []
        try:
    
            email = request.authorization['username']

        except Exception:
            email = None

        message, status = autorization_to_servise(email).values()
        if status:
            if _is_user_is_admin(email) or json.loads(user_value).get("email") == email:
                return json.loads(user_value)

            else:
                _temp_dict = dict(json.loads(user_value))
                for _atr in ['email', 'name', 'favorite']:
                    _return_dict[_atr] = _temp_dict[_atr]

                return _return_dict
        else:
            _return_dict['message'] = message
            _temp_dict = dict(json.loads(user_value))
            _return_dict['name'] = _temp_dict['name']

            return _return_dict

    elif request.method == "DELETE":
        if id == '0':
            return """SUPER ADMIN CANNOT BE DELETED"""

        try:
            
            log_email = request.authorization['username']
        
        except Exception:
            return """You should autorize to delete account"""

        else:
            try:
                
                current_value = json.loads(r.get(id))
                
            except Exception:
                return f"""User with id: {id} are not exists"""

            messge, status = autorization_to_servise(log_email)
            if status:
                if log_email != current_value['email'] and not _is_user_is_admin(log_email):
                    return """Only admin can delete other user account"""
            
            try:
                r.delete(id)
        
            except Exception:
                return f"""Cannot delete user with {id}"""
            else:
                return f"""User with id: {id} succesfulle deleted"""

    return """Id doesn't exists"""

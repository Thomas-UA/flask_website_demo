from flask import session
from src.api import app
from src.api.autorization import create_user_builder, decode_auth_token
from src.api.roles import NonRegistered, Registered
from src.db.helpers import delete_user_db
from src.redis.init_db import r


@app.route("/delete_user", methods=["GET"])
def delete_user():
    if not session["token"]:
        return "You should login to delete account"

    username = decode_auth_token(session["token"])
    return delete_user_db(username)

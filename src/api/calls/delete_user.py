from src.api import app
from src.api.autorization import create_user_builder
from src.api.permissions import is_user_owner
from src.api.roles import Admin, NonRegistered
from src.db.helpers import delete_user_db
from src.redis.init_db import r


@app.route("/delete_user/<string:user_name>", methods=["DELETE"])
def delete_user(user_name):
    return delete_user_db(user_name)

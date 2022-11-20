from src.api import app
from src.api.autorization import create_user_builder
from src.api.roles import NonRegistered, Registered
from src.db.helpers import delete_user_db
from src.redis.init_db import r


@app.route("/delete_user/<string:user_name>", methods=["DELETE"])
def delete_user(user_name):
    user_session = create_user_builder()
    if type(user_session) is not Registered:
        return f"Please login to delete account"

    if user_session.is_user_owner(user_name):
        return f"You can't delete other users account"

    return delete_user_db(user_name)

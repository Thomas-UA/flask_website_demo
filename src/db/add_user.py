from sqlalchemy import text
from src.db.connection import engine
from src.models.users import UserModel


def add_user_to_db(uname: str, pwhash: bytes):
    user = UserModel(
        uname=uname,
        pwhash=pwhash.decode('utf-8')
    )
    with engine.connect() as conn:
        conn.execute(text(
            f"INSERT INTO flask_users (uname, pwhash, favorite, registration_date)"
            f"VALUES('{user.uname}', '{user.pwhash}', '{user.favorite}', '{user.registration_date}');")
        )

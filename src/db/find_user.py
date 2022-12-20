from sqlalchemy import text
from src.db.connection import engine


def get_pwhash_by_username(uname: str):
    with engine.connect() as conn:
        pwhash = conn.execute(text(f"SELECT pwhash FROM flask_users WHERE uname='{uname}'"))
        return pwhash.fetchone()


def is_user_registered_in_db(uname: str):
    with engine.connect() as conn:
        user_info = conn.execute(text(f"SELECT uname FROM flask_users WHERE uname='{uname}'"))
        if not user_info.fetchone():
            return False

        return True


def find_users_by_username(uname: str):
    with engine.connect() as conn:
        users = conn.execute(text(f"SELECT uname FROM flask_users WHERE uname LIKE '%{uname}%'"))
        return users.fetchall()


def find_users_by_favorite(favorite: str):
    with engine.connect() as conn:
        users = conn.execute(text(f"SELECT uname FROM flask_users WHERE favorite LIKE '%{favorite}%'"))
        return users.fetchall()


def profile_data(uname: str, fields: list):
    with engine.connect() as conn:
        info = conn.execute(text(f"SELECT {','.join(fields)} FROM flask_users WHERE uname='{uname}'"))
        return info.fetchone()

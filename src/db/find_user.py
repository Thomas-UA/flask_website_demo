from sqlalchemy import text
from src.db.connection import engine


def get_pwhash_by_username(uname: str):
    with engine.connect() as conn:
        pwhash = conn.execute(text(f"SELECT pwhash FROM flask_users WHERE uname='{uname}'"))
        return pwhash.fetchone()


def find_user_in_db(uname: str):
    with engine.connect() as conn:
        user_info = conn.execute(text(f"SELECT uname FROM flask_users WHERE uname='{uname}'"))
        if not user_info.fetchone():
            return False

        return True


def user_data_for_page(uname: str):
    with engine.connect() as conn:
        info = conn.execute(text(f"SELECT uname, favorite FROM flask_users WHERE uname='{uname}'"))
        return info.fetchone()

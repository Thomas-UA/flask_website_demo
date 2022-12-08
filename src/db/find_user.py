from sqlalchemy import text
from src.db.connection import engine


def get_pwhash_by_username(username: str):
    with engine.connect() as conn:
        pwhash = conn.execute(text(f"SELECT pwhash FROM accounts WHERE uname='{username}'"))
        return pwhash.fetchone()


def find_user_in_db(username: str):
    with engine.connect() as conn:
        user_info = conn.execute(text(f"SELECT uname FROM accounts WHERE uname='{username}'"))
        if not user_info.fetchone():
            return False

        return True

from sqlalchemy import text
from src.db.connection import engine


def add_user_to_db(username: str, password_hash: bytes):
    with engine.connect() as conn:
        result = conn.execute(text(
            f"INSERT INTO public.accounts (uname, pwhash) VALUES('{username}', '{password_hash}');")
        )
        return result.fetchone()

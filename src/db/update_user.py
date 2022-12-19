from sqlalchemy import text
from src.db.connection import engine


def update_favorite(uname, favorite):
    with engine.connect() as conn:
        conn.execute(text(f"UPDATE flask_users SET favorite='{favorite}' WHERE uname='{uname}'"))

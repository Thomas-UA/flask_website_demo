import os
import sqlite3

from src.db.users_config import USERS


def create_db():
    table = """CREATE TABLE users (
                accountID INTEGER PRIMARY KEY AUTOINCREMENT,
                Email TEXT NOT NULL UNIQUE,
                Username TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL,
                Favorite TEXT
            );"""

    if not os.path.exists("users.db"):
        with sqlite3.connect("users.db") as db:
            cursor_obj = db.cursor()
            cursor_obj.execute(table)

            for user in USERS:
                insert_query = f"""
                    INSERT INTO users(
                        Email,
                        Username,
                        Password,
                        Favorite
                    ) VALUES (
                        "{user.get('email')}",
                        "{user.get('username')}",
                        "{user.get('password')}",
                        "{user.get('favorite', 'Not specified')}"
                    )"""
                cursor_obj.execute(insert_query)

from collections import OrderedDict
import sqlite3

from src.db.users_config import USERS


def login_by_email_helper(email: str):
    with sqlite3.connect("users.db") as db:
        cursor_obj = db.cursor()
        keys_json_db = ["username", "password"]
        try:

            database_result = cursor_obj.execute(
                f"""
                SELECT {', '.join(keys_json_db)} FROM users WHERE email="{email}"
            """
            )

        except Exception:
            raise Exception("Something going wrong")
        else:
            database_result = cursor_obj.fetchone()
            if not database_result:
                return f"User with email {email} not registered"

            return dict(zip(keys_json_db, database_result))


def get_all_user_info(fields):
    db_fields = ", ".join(fields) if fields else "*"
    with sqlite3.connect("users.db") as db:
        cursor_obj = db.cursor()
        try:

            database_result = cursor_obj.execute(
                f"""
                SELECT {db_fields} FROM users;
                """
            )

        except Exception:
            raise Exception("Something going wrong")
        else:
            database_result = cursor_obj.fetchall()
            k = list(USERS[0].keys())
            if not fields:
                k.insert(0, "id")
            return [
                dict(zip(k if not fields else fields, r)) for r in list(database_result)
            ]


def get_user_info(username: str, fields):
    db_fields = ", ".join(fields) if fields else "*"
    with sqlite3.connect("users.db") as db:
        cursor_obj = db.cursor()
        try:

            database_result = cursor_obj.execute(
                f"""
                SELECT {db_fields} FROM users WHERE Username="{username}"
                """
            )

        except Exception:
            raise Exception("Something going wrong")
        else:
            database_result = cursor_obj.fetchone()
            if not database_result:
                return None
            k = list(USERS[0].keys())
            if not fields:
                k.insert(0, "id")
            return dict(zip(k if not fields else fields, database_result))


def create_user_db(user: dict):
    with sqlite3.connect("users.db") as db:
        cursor_obj = db.cursor()

        try:

            cursor_obj.execute(
                f"""
                        INSERT INTO users(
                        Email,
                        Username,
                        Password,
                        Favorite,
                        Admin
                    ) VALUES (
                        "{user['email']}",
                        "{user['username']}",
                        "{user['password']}",
                        "{user.get('favorite', 'Do not declarated')}",
                        {user.get('admin_role', 0)}
                    )
                    """
            )

        except sqlite3.IntegrityError:
            return f"User already registered. Call to super admin if u forgot password"
        except Exception:
            raise Exception("Something going wrong")
        else:
            return f"User {user.get('username')} created"


def _generate_query(new_data: dict):
    query_to_db = "SET "
    for k in new_data.keys():
        v = new_data.get(k)
        if v:
            query_to_db += f'{k}="{v}", '
    return query_to_db[:-2]


def update_user_db(username: str, new_data: dict):
    with sqlite3.connect("users.db") as db:
        cursor_obj = db.cursor()

        set_query = _generate_query(new_data)

        try:
            q = f"""
                UPDATE users
                {set_query}
                WHERE Username="{username}"
                """
            cursor_obj.execute(q)

        except Exception:
            raise Exception("Something going wrong")
        else:
            return f"User {username} was updated"


def delete_user_db(username: str):
    with sqlite3.connect("users.db") as db:
        cursor_obj = db.cursor()

        try:

            cursor_obj.execute(
                f"""
                DELETE FROM users WHERE Username="{username}"
                """
            )

        except Exception:
            raise Exception("Something going wrong")
        else:
            return f"User {username} deleted"

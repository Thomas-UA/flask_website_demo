import sqlite3

from src.db.users_config import USERS

def get_all_user_info():
    with sqlite3.connect("users.db") as db:
        cursor_obj = db.cursor()
        try:

            database_result = cursor_obj.execute(
                f"""
                SELECT * FROM users
                """
            )

        except Exception as e:
            return f"Something going wrong. Error {e}"

        else:
            return [dict(zip(USERS[0].keys(), r)) for r in list(database_result)]

def get_user_info(username: str):
    with sqlite3.connect("users.db") as db:
        cursor_obj = db.cursor()
        try:

            database_result = cursor_obj.execute(f"""
                SELECT * FROM users WHERE Username="{username}"
            """)

        except Exception as e:
            return f"Something going wrong. Error {e}"

        else:
            database_result = cursor_obj.fetchone()
            return dict(zip(USERS[0].keys(), database_result))

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

            except Exception as e:
                return f"Something going wrong. {e}"
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
        
        current_data = get_user_info(username)
        set_query = _generate_query(new_data)

        try:
            q = f"""
                UPDATE users
                {set_query}
                WHERE Username="{username}"
                """
            cursor_obj.execute(
                q
            )
        
        except Exception as e:
            return f"Something going wrong. {e}"
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
        
        except Exception as e:
            return f"Something going wrong. {e}"
        else:
            return f"User {username} deleted"

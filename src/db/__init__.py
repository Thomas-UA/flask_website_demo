import sqlite3


def _connect_to_db():
    connection_obj = sqlite3.connect("users.db")
    cursor_obj = connection_obj.cursor()
    return cursor_obj

def get_user_info(username=None):
    if not username:
        return False

    with sqlite3.connect("users.db") as db:
        cursor_obj = db.cursor()
        try:

            database_result = cursor_obj.execute(
                f"""
                SELECT * FROM users WHERE Username="{username}"
                """
            )

        except Exception as e:
            return f"Something going wrong. Error {e}"

        else:
            database_result = cursor_obj.fetchone()
            # print(database_result[0])
            return list(database_result)
'''
def create_user(self, user: dict):
    connection_obj = _connect_to_db()

    try:

        cursor_obj.execute(
            f"""
                INSERT INTO USERS(
                Email,
                Username,
                Password,
                Favorite,
                Admin
            ) VALUES (
                {user.get("email")},
                {user.get("username")},
                {user.get("password")},
                {user.get("favorite", "Do not declarated")},
                {user.get("admin_role", "False")}
            """
        )

    except Exception:
        return False
    else:
        return True
    finally:
        self._close_connection()

def update_user(self):
    self._connect_to_db()
    self._close_connection()

def delete_user(self):
    self._connect_to_db()
    self._close_connection()
'''

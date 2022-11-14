import json

from src.redis.init_db import r


def is_user_owner(key, email):
    try:

        return email == json.loads(r.get(key)).get("email")

    except Exception:
        return False

import json
import redis

from src.redis.users_config import USERS

from datetime import datetime


r = redis.Redis(charset="utf-8", decode_responses=True, host="localhost", port=6379)


for user in USERS:
    r.set(
        name=user.get("id"),
        value=json.dumps(
            {
                "email": user.get("email"),
                "password": user.get("password"),
                "name": user.get("name"),
                "registration_date": str(datetime.now()),
                "admin_role": user.get("admin_role", False),
                "favorite": user.get("favorite", "Do not declarated")
            }
        ),
        # ex=360
    )

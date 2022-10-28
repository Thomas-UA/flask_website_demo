import json
import redis

from redis_db import USERS

from datetime import datetime


r = redis.Redis(charset="utf-8", decode_responses=True)
# host="localhost", port=6379, db=0

with r.pipeline() as pipe:
    for user in USERS:
        pipe.set(
            name=user.get("id"),
            value=json.dumps(
                {
                    "email": user.get("email"),
                    "password": user.get("password"),
                    "name": user.get("name"),
                    "registration_date": str(datetime.now())
                }
            ),
            ex=360
        )
    pipe.execute()

r.bgsave()

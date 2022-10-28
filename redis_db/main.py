import json
import redis

from redis_db.db import USERS

from datetime import datetime


r = redis.Redis()

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

r.bgsave()

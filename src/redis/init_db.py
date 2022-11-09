import json
import redis


from datetime import datetime


r = redis.Redis(charset="utf-8", decode_responses=True, host="localhost", port=6379)

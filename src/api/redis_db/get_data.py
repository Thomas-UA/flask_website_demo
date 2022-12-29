from src.api.redis_db.connection import redis_connection


def get_data(key=None):
    if key is None:
        return None

    return redis_connection.get(key)

from src.redis_db.connection import redis_connection


def get_data():
    return redis_connection.keys()

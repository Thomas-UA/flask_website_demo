from flask import current_app

from src.redis_db.connection import redis_connection


def set_new_data(data_dict):
    current_app.logger.info(f"New data: {data_dict}")
    for key, value in data_dict.items():
        redis_connection.set(key, value, 600)

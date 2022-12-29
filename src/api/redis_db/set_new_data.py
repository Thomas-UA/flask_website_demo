from src.api.redis_db.connection import redis_connection


def set_new_data(data_dict=None):
    if data_dict is None:
        data_dict = {"foo": "bar"}
    with redis_connection.pipeline() as pipe:
        for key, value in data_dict.items():
            pipe.set(key, value)
        pipe.execute()

import logging
from sqlalchemy import text
from src.db.connection import engine


def create_psql_db():
    with engine.connect() as conn:
        logging.info("Connected to postgres db")
        # conn.execution_options(isolation_level="AUTOCOMMIT").execute('''CREATE DATABASE flask_web_site''')
        logging.info("flask_web_site db created")
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(
            text(
                ''' CREATE TABLE IF NOT EXISTS flask_users (
                        id SERIAL PRIMARY KEY,
                        uname varchar(200) UNIQUE NOT NULL,
                        pwhash varchar(512) NOT NULL
                    )
                '''
            )
        )

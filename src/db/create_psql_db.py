import logging
from sqlalchemy import text
from src.db.connection import engine


def create_psql_db():
    with engine.connect() as conn:
        logging.info("Connected to postgres db")
        logging.info("flask_web_site db created")
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(
            text(
                ''' CREATE TABLE IF NOT EXISTS flask_users (
                        id SERIAL PRIMARY KEY,
                        uname text UNIQUE NOT NULL,
                        pwhash text NOT NULL,
                        favorite text,
                        registration_date timestamp
                    )
                '''
            )
        )

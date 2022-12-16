import sqlalchemy


engine = sqlalchemy.create_engine("postgresql://postgres:postgrespw@postgres_db:5432")

import sqlalchemy


engine = sqlalchemy.create_engine("postgresql://postgres:postgrespw@localhost:49153/flask_web_site")

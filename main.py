from src.app import app
from src.db.create_psql_db import create_psql_db


if __name__ == "__main__":
    create_psql_db()
    app.run(host="0.0.0.0", debug=True, port=8080)

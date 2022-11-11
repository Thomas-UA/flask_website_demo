from src.api import app
from src.api.autorization import autorize_to_system


@app.route("/login", methods=["GET"])
def login_to_server():
    return autorize_to_system()

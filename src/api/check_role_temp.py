from flask import request
from src.api import app


@app.route("/check")
def check_role():
    head = request.headers.environ
    token = head.get("HTTP_AUTHORIZATION")[7:]
    return token

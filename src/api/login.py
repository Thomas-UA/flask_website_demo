from flask import Response, redirect, render_template, request, session
from src.api import app
from src.api.autorization import (
    AuthenticationError,
    autorize_to_system,
    decode_auth_token,
    encode_auth_token,
)
from src.api.calls.get_user import get_user_by_id


@app.route("/login", methods=["GET", "POST"])
def login_to_server():
    if request.method == "POST":
        try:

            user_seesion_token = autorize_to_system()

        except Exception:
            return Response(status=401)

        username = decode_auth_token(user_seesion_token)
        session["token"] = user_seesion_token
        return redirect(f"/user/{username}")
    return render_template("login.html")

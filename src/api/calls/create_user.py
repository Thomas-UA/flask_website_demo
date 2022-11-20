from datetime import datetime
import json

from src.api import app
from src.api.login import login_to_server
from src.db.helpers import create_user_db
from src.redis.init_db import r

from flask import render_template, request


@app.route("/register", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = email.split("@")[0] if not request.form["username"] else request.form["username"]
        favorite = 'Not specified' if not request.form["favorite"] else request.form["favorite"]

        is_user_has_created = create_user_db(
            {
                "email": email,
                "username": username,
                "password": password,
                "favorite": favorite,
            }
        )

        if not is_user_has_created:
            return render_template("profile.html", user=f"User {username} is already registered")

        else:
            return login_to_server()

    return render_template("register.html")

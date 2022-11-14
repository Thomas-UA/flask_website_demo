from flask import redirect, session
from src.api import app


@app.route("/logout")
def logout():
    session["token"] = None
    return redirect("/")

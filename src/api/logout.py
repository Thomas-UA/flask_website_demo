from flask import redirect, session
from src.api import app


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

from flask import render_template
from src.api import app


@app.route("/")
@app.route("/hw")
@app.route("/hello")
@app.route("/hello_world")
@app.route("/world")
def home_page():
    return render_template("index.html"), 200

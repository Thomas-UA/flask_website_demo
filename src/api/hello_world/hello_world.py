from src.api import app


@app.route("/")
@app.route("/hw")
@app.route("/hello")
@app.route("/hello_world")
@app.route("/world")
def home_page():
    return "Hello world"

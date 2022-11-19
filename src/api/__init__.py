from flask import Flask, session

app = Flask(__name__, template_folder="../../templates")
app.config["SECRET_KEY"] = "secret_string"

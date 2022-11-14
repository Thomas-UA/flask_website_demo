from flask import Flask, session

app = Flask(__name__, template_folder="/home/pi/flask_api_service/templates")
app.config['SECRET_KEY'] = "secret_string"

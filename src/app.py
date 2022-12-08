from cryptography.fernet import Fernet
from flask import Flask

from src.api.auth.register import register_blueprint
from src.api.hello_world import hello_world_blueprint
from src.api.index import index_blueprint
from src.api.auth.login import login_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = Fernet.generate_key()
app.register_blueprint(hello_world_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(register_blueprint)

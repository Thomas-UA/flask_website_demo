from flask import Flask
from src.api.hello_world import hello_world_blueprint
from src.api.index import index_blueprint

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.register_blueprint(hello_world_blueprint)
app.register_blueprint(index_blueprint)

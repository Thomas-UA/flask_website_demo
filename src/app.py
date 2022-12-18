from cryptography.fernet import Fernet
from flask import Flask

from src.api.auth.register import signup_blueprint
from src.api.hello_world import hello_world_blueprint
from src.api.index import index_blueprint
from src.api.auth.login import login_blueprint
from src.api.logout import logout_from_site
from src.api.profile import my_profile_blueprint, user_profile_blueprint
from src.api.search import search_blueprint_username, search_blueprint_favorite

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = Fernet.generate_key()
app.register_blueprint(hello_world_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(signup_blueprint)
app.register_blueprint(my_profile_blueprint)
app.register_blueprint(logout_from_site)
app.register_blueprint(search_blueprint_username)
app.register_blueprint(search_blueprint_favorite)
app.register_blueprint(user_profile_blueprint)

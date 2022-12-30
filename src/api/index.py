from flask import Blueprint, render_template, current_app

from src.redis_db.get_data import get_data

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/', methods=['GET'])
def index_page():
    current_app.logger.info("Returning index page")
    last_registered_users = get_data()
    current_app.logger.info(f"Last registered users: {last_registered_users}")
    return render_template('index.html', last_registered_users=last_registered_users)

from flask import Blueprint, render_template, current_app

index_blueprint = Blueprint('index_blueprint', __name__)


@index_blueprint.route('/', methods=['GET'])
def index_page():
    current_app.logger.info("Returning index page")
    return render_template('index.html')

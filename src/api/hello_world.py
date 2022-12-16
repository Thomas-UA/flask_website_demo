from flask import Blueprint, render_template, current_app

hello_world_blueprint = Blueprint('hello_world_blueprint', __name__)


@hello_world_blueprint.route('/hello_world', methods=['GET'])
def hello_world_page():
    current_app.logger.info("Returning hello world page")
    return render_template('hello_world.html', hello_world="Hello World")

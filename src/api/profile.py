from flask import Blueprint, render_template, current_app

user_profile_blueprint = Blueprint('user_profile_blueprint', __name__)


@user_profile_blueprint.route('/profile', methods=['GET'])
def profile_page():
    user = "user"
    current_app.logger.info("Opening profile page")
    return render_template('profile.html', user=user)

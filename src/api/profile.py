from flask import Blueprint, render_template, current_app, session

from src.db.find_user import user_data_for_page
from src.models.users import UserFront

user_profile_blueprint = Blueprint('user_profile_blueprint', __name__)


@user_profile_blueprint.route('/profile', methods=['GET'])
def profile_page():
    user = session.get("token")
    current_app.logger.info("Opening profile page")
    info = user_data_for_page(user)
    current_app.logger.info(f"User info: {info}")
    return render_template('profile.html', user=info)

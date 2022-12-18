from flask import Blueprint, render_template, current_app, session, redirect

from src.db.find_user import my_profile_data, user_profile_data

my_profile_blueprint = Blueprint('my_profile_blueprint', __name__)
user_profile_blueprint = Blueprint('user_profile_blueprint', __name__)


@my_profile_blueprint.route('/profile', methods=['GET'])
def my_profile_page():
    user = session.get("token")
    current_app.logger.info("Opening profile page")
    info = my_profile_data(user)
    current_app.logger.info(f"User info: {info}")
    return render_template('profile.html', user=info)


@user_profile_blueprint.route('/profile/<user>', methods=['GET'])
def user_profile_page(user):
    if user == session.get("token"):
        return redirect('/profile')

    info = user_profile_data(user)
    current_app.logger.info(f"User info: {info}")
    return render_template('profile.html', user=info)

from flask import Blueprint, render_template, current_app, session, redirect, request

from src.db.find_user import profile_data
from src.db.update_user import update_favorite

my_profile_blueprint = Blueprint('my_profile_blueprint', __name__)
user_profile_blueprint = Blueprint('user_profile_blueprint', __name__)


@my_profile_blueprint.route('/profile', methods=['GET', 'POST'])
def my_profile_page():
    user = session.get("token")
    if request.method == 'POST':
        favorite = request.form.get('favorite')
        update_favorite(user, favorite)
        return redirect('/profile')

    current_app.logger.info("Opening profile page")
    info = profile_data(user)
    current_app.logger.info(f"User info: {info}")
    return render_template('my_profile.html', user=info)


@user_profile_blueprint.route('/profile/<user>', methods=['GET'])
def user_profile_page(user):
    if user == session.get("token"):
        return redirect('/profile')

    info = profile_data(user)
    current_app.logger.info(f"User info: {info}")
    return render_template('profile.html', user=info)

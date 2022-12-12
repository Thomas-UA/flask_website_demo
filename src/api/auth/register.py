from cryptography.fernet import Fernet

from flask import Blueprint, render_template, request, current_app, redirect

from src.db.find_user import find_user_in_db
from src.db.add_user import add_user_to_db

signup_blueprint = Blueprint('signup_blueprint', __name__)


@signup_blueprint.route('/signup', methods=['GET', 'POST'])
def signup_page():
    current_app.logger.info(f"Request method: {request.method}")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        current_app.logger.info(f"Username: {username}")
        current_app.logger.info(f"Password: {password}")

        current_app.logger.info(f"Trying to find user in db: {username}")
        is_user_registered = find_user_in_db(username)
        if is_user_registered:
            current_app.logger.info(f"User: {username} already registered")

        pwhash = Fernet(current_app.secret_key).encrypt(bytes(password.encode()))
        add_user_to_db(username, pwhash)

        redirect('/profile')

    return render_template('register.html')

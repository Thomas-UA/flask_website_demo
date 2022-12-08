from cryptography.fernet import Fernet

from flask import Blueprint, render_template, request, current_app

from src.db.find_user import get_pwhash_by_username

login_blueprint = Blueprint('login_blueprint', __name__)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    current_app.logger.info(f"Request method: {request.method}")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        current_app.logger.info(f"Username: {username}")
        current_app.logger.info(f"Password: {password}")

        current_app.logger.info(f"Getting pwhash of user: {username}")
        pwhash = get_pwhash_by_username(username)

        if not pwhash:
            current_app.logger.info(f"User {username} not registered")

        password_hash = Fernet(current_app.secret_key).encrypt(bytes(password.encode()))
        if password_hash != pwhash:
            current_app.logger.info(f"Password is incorrect")

    return render_template('login.html')

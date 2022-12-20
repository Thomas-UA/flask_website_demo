from cryptography.fernet import Fernet

from flask import Blueprint, render_template, request, current_app, session, redirect

from src.db.find_user import get_pwhash_by_username

login_blueprint = Blueprint('login_blueprint', __name__)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    current_app.logger.info(f"Request method: {request.method}")
    if request.method == 'POST':
        uname = request.form.get('uname')
        password = request.form.get('password')

        current_app.logger.info(f"Username: {uname}")
        current_app.logger.info(f"Password: {password}")

        current_app.logger.info(f"Getting pwhash of user: {uname}")
        pwhash = get_pwhash_by_username(uname)

        if not pwhash:
            current_app.logger.info(f"User {uname} not registered")

        password_hash = Fernet(current_app.secret_key).encrypt(bytes(password.encode()))
        if password_hash != pwhash:
            current_app.logger.info(f"Password is incorrect")

        session["token"] = uname
        return redirect(f"/profile/{uname}")

    return render_template('login.html')

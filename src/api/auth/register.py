from cryptography.fernet import Fernet

from flask import Blueprint, render_template, request, current_app, redirect, session

from src.db.find_user import is_user_registered_in_db
from src.db.add_user import add_user_to_db

signup_blueprint = Blueprint('signup_blueprint', __name__)


@signup_blueprint.route('/signup', methods=['GET', 'POST'])
def signup_page():
    current_app.logger.info(f"Request method: {request.method}")
    if request.method == 'POST':
        uname = request.form.get('uname')
        password = request.form.get('password')

        current_app.logger.info(f"Username: {uname}")
        current_app.logger.info(f"Password: {password}")

        current_app.logger.info(f"Trying to find user in db: {uname}")
        is_user_registered = is_user_registered_in_db(uname)
        if is_user_registered:
            current_app.logger.info(f"User: {uname} already registered")
            return redirect('/')

        pwhash = Fernet(current_app.secret_key).encrypt(bytes(password.encode()))
        add_user_to_db(uname, pwhash)

        session["token"] = uname
        return redirect('/profile')

    return render_template('register.html')

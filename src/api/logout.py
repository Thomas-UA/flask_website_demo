from flask import current_app, Blueprint, redirect, session

logout_from_site = Blueprint("logout_from_site", __name__)


@logout_from_site.route('/logout', methods=['GET'])
def logout():
    current_app.logger.info("Logout from site")
    session['token'] = None
    return redirect("/")

from flask import current_app, Blueprint, redirect

logout_from_site = Blueprint("logout_from_site", __name__)


@logout_from_site.route('/logout', methods=['GET'])
def logout():
    current_app.logger.info("Logout from site")
    return redirect("/")

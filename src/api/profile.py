from flask import Blueprint, render_template, current_app, session

from src.api.auth.user_role import user_factory
from src.db.find_user import profile_data

my_profile_blueprint = Blueprint('my_profile_blueprint', __name__)
user_profile_blueprint = Blueprint('user_profile_blueprint', __name__)


@user_profile_blueprint.route('/profile/<user>', methods=['GET', 'POST'])
def user_profile_page(user):
    uname = session.get("token", None)
    current_app.logger.info(f"Current user: {uname}")

    user_session = user_factory(uname)
    current_app.logger.info(f"User type: {str(user_session)}")
    user_info = profile_data(user, user_session.fields)
    current_app.logger.info(f"User user_info: {user_info}")
    try:

        is_user_owner = user_session.is_user_owner(user)
        current_app.logger.info(f"Is user owner: {is_user_owner}")

    except NotImplementedError:
        pass

    else:
        if is_user_owner:
            return render_template('my_profile.html', user=user_info)

    return render_template('profile.html', user=user_info)

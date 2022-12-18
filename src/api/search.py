from flask import Blueprint, render_template, current_app, redirect

from src.db.find_user import find_users_by_username, find_users_by_favorite

search_blueprint_username = Blueprint('search_blueprint_username', __name__)
search_blueprint_favorite = Blueprint('search_blueprint_favorite', __name__)


@search_blueprint_username.route('/search_by_username/<username>', methods=['GET'])
def find_users_by_username_front(username):
    if not username:
        return redirect('/')
    current_app.logger.info(f"Criteria: {username}")
    list_of_users = find_users_by_username(username)
    current_app.logger.info(f"List of users by {username}: {list_of_users}")
    return render_template('search_result.html', list_of_users=list_of_users)


@search_blueprint_favorite.route('/search_by_favorite/<favorite>', methods=['GET'])
def find_users_by_username_front(favorite):
    if not favorite:
        return redirect('/')
    current_app.logger.info(f"Criteria: {favorite}")
    list_of_users = find_users_by_favorite(favorite)
    current_app.logger.info(f"List of users by {favorite}: {list_of_users}")
    return render_template('search_result.html', list_of_users=list_of_users)

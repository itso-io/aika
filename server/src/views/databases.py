from flask import Blueprint, session, request, jsonify
from flask_login import login_required, current_user

from controllers.databases import get_user_database

databases = Blueprint('databases', __name__)

@databases.route('/api/databases/mine')
@login_required
def get_my_database():
  user_database = get_user_database(current_user)

  return jsonify({
    'host': user_database.host,
    'port': user_database.port,
    'username': user_database.username,
    'password': user_database.password,
    'name': user_database.database
  })

from flask import Blueprint, session, request, jsonify

databases = Blueprint('databases', __name__)

@databases.route('/api/databases/mine')
def get_user_database():
  return jsonify({
    'host': '127.0.0.1',
    'username': 'user_123',
    'password': 'Holbewoner1987!',
    'name': 'my_database'
  })

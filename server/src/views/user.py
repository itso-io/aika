from flask import request, Blueprint, json, jsonify, session
from flask_login import login_required, current_user
import pymysql

# from utils.database import new_alchemy_encoder
from utils.app import jsonify, new_alchemy_encoder
from utils.errors import APIError
from controllers.user import get_user_email as controller_get_user_email
from controllers.user import get_user_id as controller_get_user_id


user = Blueprint('user', __name__)


@user.route('/api/users/<int:user_id>')
def get_user_id(user_id):
    try:
        return jsonify(controller_get_user_id(user_id))
    except APIError as err:
        return err.as_response()


@user.route('/api/users/<string:email>')
def get_user_email(email):
    try:
        return jsonify(controller_get_user_email(email))
    except APIError as err:
        return err.as_response()


@user.route('/api/users/me')
@login_required
def get_current_user():
    return jsonify(None if not current_user else {'email': current_user.email})

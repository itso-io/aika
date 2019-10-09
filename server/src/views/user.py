
from flask import request, Blueprint, json
import pymysql

# from utils.database import new_alchemy_encoder
from utils.app import jsonify, new_alchemy_encoder
from utils.errors import APIError
from controllers.user import create_user as controller_create_user
from controllers.user import get_user as controller_get_user


user = Blueprint('user', __name__)


@user.route('/api/create-user')
def create_user():
    """Add a row to the User table"""
    email = request.args.get('email')
    try:
        return jsonify(controller_create_user(email))
    except APIError as err:
        return err.as_response()


@user.route('/api/get-user')
def get_user():
    email = request.args.get('email')
    try:
        return jsonify(controller_get_user(email))
    except APIError as err:
        return err.as_response()


import json

from flask import jsonify, request, Blueprint
import pymysql

from utils.database import new_alchemy_encoder
from controllers.user import create_user as controller_create_user
from controllers.user import get_user as controller_get_user

user = Blueprint('user', __name__)


@user.route('/create-user')
def create_user():
    """Add a row to the User table"""

    email = request.args.get('email')
    user = controller_create_user(email)

    udb_dict = json.loads(json.dumps(
        user, cls=new_alchemy_encoder(False), check_circular=False))

    return jsonify(udb_dict)


@user.route('/get-user')
def get_user():
    email = request.args.get('email')

    udb = controller_get_user(email)
    udb_dict = json.loads(json.dumps(
        udb, cls=new_alchemy_encoder(False), check_circular=False))

    return jsonify(udb_dict)


import json
import logging

from flask import jsonify, request, Blueprint
from sqlalchemy_utils import database_exists, drop_database, create_database
import pymysql

from models.base import db
from models.app_main import User, UserDatabase
from utils.common import random_password
from utils.database import get_db_url, email_to_name, new_alchemy_encoder
from utils.app import app


user = Blueprint('user', __name__)

@user.route('/create-user')
def create_user_and_database():
    """Add a row to the User table"""

    new_db_name = email_to_name(request.args.get('email'))
    new_password = random_password()


    user = User(email=request.args.get('email'))
    tmp_database_root = UserDatabase(
        drivername='mysql+pymysql',
        username='root',
        password='Holbewoner1987!',
        host='127.0.0.1',
        port=3306,
        database=new_db_name,
        query='test'
    )
    new_database = UserDatabase(
        drivername='mysql+pymysql',
        username=new_db_name,
        password=new_password,
        host='127.0.0.1',
        port=3306,
        database=new_db_name,
        query='test',
        user=user
    )
    url = get_db_url(tmp_database_root)

    if not database_exists(url):
        create_database(url)
    
    priveleges = [
        'CREATE',
        'INSERT',
        'SELECT',
        'UPDATE'
    ]

    priveleges_string = ', '.join(priveleges)

    app.config['SQLALCHEMY_BINDS']['user_db'] = url
    db.create_all(['user_db'])

    try:
        create_user_query = f'CREATE USER \'{new_db_name}\'@\'localhost\' IDENTIFIED BY \'{new_password}\';'
        db.engine.execute(create_user_query)
    except Exception as err:
        logging.warn(err)
    
    grant_perms_query = f'GRANT {priveleges_string} ON {new_db_name}.* TO \'{new_db_name}\'@\'localhost\';'
    db.engine.execute(grant_perms_query)

    db.session.add(user)
    db.session.commit()

    udb_dict = json.loads(json.dumps(user, cls=new_alchemy_encoder(False), check_circular=False))
    
    return jsonify(udb_dict)
    return jsonify({})


@user.route('/get-user')
def get_user():
    email = request.args.get('email')

    udb = db.session.query(User).filter(User.email == email).one_or_none()
    udb_dict = json.loads(json.dumps(udb, cls=new_alchemy_encoder(False), check_circular=False))
    
    return jsonify(udb_dict)
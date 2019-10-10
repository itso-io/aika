import logging

from sqlalchemy_utils import database_exists, drop_database, create_database
from sqlalchemy.orm.exc import NoResultFound

from utils.database import get_db_url, email_to_name
from models.base import db
from utils.app import app
from utils.enums import APIErrorTypes
from utils.common import random_password
from utils.validators import is_email
from models.app_main import User, UserDatabase


from utils.errors import APIError


# TODO create Metabase user
def create_user(email):
    if not is_email(email):
        raise APIError(
            http_code=409,
            error_type_key=APIErrorTypes.invalid_email,
            message=f'Invalid input. {email} is not a valid email'
        )
    new_db_name = email_to_name(email)
    new_password = random_password()

    if User.query.filter_by(email=email).count() > 0:
        raise APIError(
            http_code=409,
            error_type_key=APIErrorTypes.user_already_exists,
            message=f'A user with email {email} already exists'
        )

    user = User(email=email)

    # Create a user that will have access to the new datase
    new_database = UserDatabase(
        drivername='mysql+pymysql',
        username=new_db_name,
        password=new_password,
        host=app.config["APP_DB_HOST"],
        port=app.config["APP_DB_PORT"],
        database=new_db_name,
        query=app.config["CLOUD_SQL_CONNECTION_NAME"],
        user=user
    )

    url = get_db_url({
        'drivername': 'mysql+pymysql',
        'username': app.config["APP_DB_USER"],
        'password': app.config["APP_DB_PASS"],
        'host': app.config["APP_DB_HOST"],
        'port': app.config["APP_DB_PORT"],
        'database': new_db_name,
        'query': app.config["CLOUD_SQL_CONNECTION_NAME"]
    })

    # Step 1: create the new database
    if database_exists(url):
        raise APIError(
            http_code=409,
            error_type_key=APIErrorTypes.database_already_exists,
            message=f'Trying to create database {new_db_name} for user {email}, but the database already exists'
        )
    else:
        create_database(url)

    # Step 2: create all the tables in the new database
    # Setting the config to the new database url is a hack
    # to make sure SQLALCHAMY does all the heavy lifting
    app.config['SQLALCHEMY_BINDS']['user_db'] = url
    db.create_all(['user_db'])

    # Step 3: Create the new user so that someone can connect
    create_user_query = f'CREATE USER \'{new_db_name}\'@\'%%\' ' \
                        f'IDENTIFIED BY \'{new_password}\';'
    db.engine.execute(create_user_query)

    # Step 4: Give the user the right privileges
    priveleges = [
        'CREATE',
        'INSERT',
        'SELECT',
        'UPDATE',
        'ALTER',
        'DROP',
        'REFERENCES'
    ]
    priveleges_string = ', '.join(priveleges)

    grant_perms_query = f'GRANT {priveleges_string} ON {new_db_name}.* ' \
                        f'TO \'{new_db_name}\'@\'%%\';'

    print(grant_perms_query)
    db.engine.execute(grant_perms_query)

    

    # Step 5: Create the alembic table for migration purposes
    alembic_create_query = f'CREATE TABLE `{new_db_name}`.`alembic_version` ' \
                           f'(' \
                           f'  `version_num` varchar(32) NOT NULL,' \
                           f'  PRIMARY KEY (`version_num`)' \
                           f')'
    db.engine.execute(alembic_create_query)

    # Step 6: Get the data that should be in the new alembic table
    alembic_select_query = f'SELECT `version_num` FROM ' \
                           f'`{app.config["EXAMPLE_DB_NAME"]}`.alembic_version'
    versions = db.engine.execute(alembic_select_query).fetchall()

    # Step 7: Insert the data into the new alembic table
    if len(versions) > 0:
        alembic_insert_query = f'INSERT INTO `{new_db_name}`.' \
                               f'`alembic_version` ' \
                               f'(`version_num`)\n' \
                               f'VALUES\n'
        for row in versions:
            alembic_insert_query += f'(\'{row[0]}\')'
        db.engine.execute(alembic_insert_query)

    # Step 8: Add the user to the session. As the relationship
    # to a UserDatabase object is created in the new_database creation,
    # adding the User object user to the session and committing it will
    # create a new User and UserDatabase row
    db.session.add(user)
    db.session.commit()

    return user


def get_user_email(email):
    if not is_email(email):
        raise APIError(
            http_code=409,
            error_type_key=APIErrorTypes.user_not_found,
            message=f'Invalid ID supplied. {email} is not a valid ID nor a '
                    f'valid email address'
        )

    try:
        return User.query.filter_by(email=email).one()
    except NoResultFound:
        raise APIError(
            http_code=404,
            error_type_key=APIErrorTypes.user_not_found,
            message=f'Can\'t find a user with the email {email}'
        )


def get_user_id(id):
    try:
        return User.query.filter_by(id=id).one()
    except NoResultFound:
        raise APIError(
            http_code=404,
            error_type_key=APIErrorTypes.user_not_found,
            message=f'Can\'t find a user with the id {id}'
        )

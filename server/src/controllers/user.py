import logging

from sqlalchemy_utils import database_exists, drop_database, create_database

from utils.database import get_db_url, email_to_name
from models.base import db
from utils.app import app
from utils.common import random_password
from models.app_main import User, UserDatabase


def create_user(email):
    new_db_name = email_to_name(email)
    new_password = random_password()

    user = User(email=email)

    # Create a temporary user that we won't save with
    # create database privileges to get a database URL
    # that will create the new database. This user
    # will not be stored, just used to create a url.
    tmp_database_root = UserDatabase(
        drivername='mysql+pymysql',
        username=app.config["APP_DB_USER"],
        password=app.config["APP_DB_PASS"],
        host=app.config["APP_DB_HOST"],
        port=app.config["APP_DB_PORT"],
        database=new_db_name,
        query=app.config["CLOUD_SQL_CONNECTION_NAME"]
    )

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
    url = get_db_url(tmp_database_root)

    # Step 1: create the new database
    if not database_exists(url):
        create_database(url)

    # Step 2: create all the tables in the new database
    app.config['SQLALCHEMY_BINDS']['user_db'] = url
    db.create_all(['user_db'])

    # Step 3: Create the new user so that someone can connect
    try:
        create_user_query = f'CREATE USER \'{new_db_name}\'@\'localhost\' ' \
                            f'IDENTIFIED BY \'{new_password}\';'
        db.engine.execute(create_user_query)
    except Exception as err:
        logging.warn(f'The database failed to create user {new_db_name} with '
                     f'the following error:')
        logging.warn(err)
        logging.warn(f'As it likely failed because a user already existed, '
                     f'we will continue')

    # Step 4: Give the user the right privileges
    priveleges = [
        'CREATE',
        'INSERT',
        'SELECT',
        'UPDATE',
        'ALTER'
    ]
    priveleges_string = ', '.join(priveleges)

    grant_perms_query = f'GRANT {priveleges_string} ON {new_db_name}.* ' \
                        f'TO \'{new_db_name}\'@\'localhost\';'
    db.engine.execute(grant_perms_query)

    # Step 5: Create the alembic table for migration purposes
    alembic_create_query = f'CREATE TABLE `{new_db_name}`.`alembic_version` (' \
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
        alembic_insert_query = f'INSERT INTO `{new_db_name}`.`alembic_version` (`version_num`)\n' \
                               f'VALUES\n'
        for row in versions:
            alembic_insert_query += f'(\'{row[0]}\')'
        db.engine.execute(alembic_insert_query)

    db.session.add(user)
    db.session.commit()

    return user


def get_user(email):
    return db.session.query(User).filter(User.email == email).one_or_none()

# Native
import re
import json

# Installed
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.engine.url import URL as SqlAlchemyURL
from flask_sqlalchemy import BaseQuery


# From app
from models.base import db
from models.app_main import UserDatabase

# for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class']:

def new_alchemy_encoder(revisit_self = False, fields_to_expand = ['user']):
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):

        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}

                # TODO filter out non supported objects like functions
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class']:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)


    return AlchemyEncoder

def get_db_url(user_database):
    return str(SqlAlchemyURL(
        drivername=user_database.drivername,
        username=user_database.username,
        password=user_database.password,
        database=user_database.database,
        host=user_database.host,
        port=user_database.port,
        # query={
        #   'unix_socket': '/cloudsql/{}'.format(user_database.query)
        # }
    ))

def get_all_user_db_urls():
    user_database_urls = {}
    databases = db.session.query(UserDatabase)
    for database in databases:
        url = get_db_url(database)
        user_database_urls[database.user.email] = url
    return user_database_urls

EMAIL_REGEX = re.compile(r"[\.\/\\@]", re.IGNORECASE)
def email_to_name(email):
    return re.sub(EMAIL_REGEX, '_', email)
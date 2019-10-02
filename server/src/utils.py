import os
from logging.config import dictConfig
import logging
from dotenv import load_dotenv
import yaml
import sqlalchemy
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_file_full_path(relative_to_root):
  return os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_to_root)

def set_config_db(app):
  db_user = app.config["DB_USER"]
  db_pass = app.config["DB_PASS"]
  db_name = app.config["DB_NAME"]
  db_host = app.config["DB_HOST"]
  db_port = app.config["DB_PORT"]
  cloud_sql_connection_name = app.config["CLOUD_SQL_CONNECTION_NAME"]

  url = str(sqlalchemy.engine.url.URL(
      drivername='mysql+pymysql',
      username=db_user,
      password=db_pass,
      database=db_name,
      host=db_host,
      port=db_port,
      # query={
      #   'unix_socket': '/cloudsql/{}'.format(cloud_sql_connection_name)
      # }
  ))
  app.config['SQLALCHEMY_DATABASE_URI'] = url
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def set_config(app):
  load_dotenv()
  dirname = os.path.dirname(__file__)
  app_filename = 'app.yaml'
  stream = open(os.path.join(dirname, app_filename), 'r')

  env_vars = {}
  logging.info('The following environment variables need to be defined for '
               'the app to run (as per app.yaml) and can be accessed through app.config[VARIABLE]:')
  for variable, app_val in yaml.load(stream, Loader)['env_variables'].items():
    value = os.getenv(variable)
    env_vars[variable] = value
    if value:
      logging.info(f'- {variable} is set from a local environment variable')
      app.config[variable] = value
    elif app_val != 'placeholder': 
      logging.info(f'- {variable} does not have to be overwritten as it isn\'t a placeholder')
      app.config[variable] = app_val
    else: 
      logging.error(f'- {variable} environment variable is NOT set')
  logging.info('')
  logging.info('You can either set them manually on your local machine, or add '
               'a .env file to the {GIT_ROOT}/server directory')
  set_config_db(app)




def set_logging(app):
  dictConfig({
      'version': 1,
      'formatters': {'default': {
          'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
      }},
      'handlers': {'wsgi': {
          'class': 'logging.StreamHandler',
          'stream': 'ext://flask.logging.wsgi_errors_stream',
          'formatter': 'default'
      }},
      'root': {
          'level': 'INFO' if app.config['DEBUG'] else 'WARNING',
          'handlers': ['wsgi']
      }
  })
  logging.info('Log information loaded')


import os
import logging
import json

from flask_sqlalchemy import SQLAlchemy as FlaskSQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import ProgrammingError

from models.base import db
from models.user_calendar import Events, EventAttendees

from utils.app import app
from utils.logging import set_logging
from utils.config import set_config, load_customer_db_config
from utils.database import get_all_user_db_urls
from views import blueprints

set_logging(app)
set_config(app)

db.init_app(app)

with app.app_context():
    try:
        load_customer_db_config(app)
    except ProgrammingError:
        logging.warn('The tables aren\'t defined yet')
    migrate = Migrate(app, db)


@app.route('/')
def hello():
    return 'Hello World!'


for blueprint in blueprints:
    app.register_blueprint(blueprint)


if __name__ == '__main__':
    # See https://cloud.google.com/appengine/docs/standard/python3/runtime
    debug_setting = os.getenv('GAE_SERVICE') != 'default'
    app.run(host='localhost', port=5000, debug=debug_setting)

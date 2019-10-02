import os

from utils import set_logging, set_config
from flask import Flask
from auth import auth
import logging
from flask_sqlalchemy import SQLAlchemy as FlaskSQLAlchemy
from flask_migrate import Migrate
from models.shared import db
from models.user import User
from models.imported_calendar import Events, EventAttendees


app = Flask(__name__)
set_logging(app)
set_config(app)

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/test-insert')
def test_insert_handler():
    """Add a row to the User table"""
    ed_user = User(name='ed', test='edsnickname', test_2='sdfsdf')
    db.session.add(ed_user)
    db.session.commit()
    
    return f'{ed_user.name} added to the database'


app.register_blueprint(auth)


if __name__ == '__main__':
    # TODO: Set debug=false if not running locally
    app.run(host='localhost', port=5000, debug=True)

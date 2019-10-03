from flask_sqlalchemy import SQLAlchemy as FlaskSQLAlchemy

db = FlaskSQLAlchemy()

class Base(db.Model):
    __abstract__ = True
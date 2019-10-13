from sqlalchemy.orm import relationship

from models.base import Base, db


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    databases = relationship("UserDatabase", back_populates="user")


class UserDatabase(Base):
    __tablename__ = 'user_databases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    drivername = db.Column(db.String(128))
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    host = db.Column(db.String(256))
    port = db.Column(db.Integer)
    database = db.Column(db.String(128))
    query = db.Column(db.String(256))
    user = relationship("User", back_populates="databases")


class Settings(Base):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    synced_calendars = db.Column(db.JSON)

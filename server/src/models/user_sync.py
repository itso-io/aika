import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.base import Base, db


class Sync(Base):
    __tablename__ = 'sync'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)


class SyncLog(Base):
    __tablename__ = 'sync_log'
    id = db.Column(db.Integer, primary_key=True)

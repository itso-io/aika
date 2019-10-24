import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.base import Base, db


class Sync(Base):
    __tablename__ = 'sync'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    synced_ids = db.Column(db.JSON)
    tasks = relationship("SyncTask", back_populates="sync")


class SyncTask(Base):
    __tablename__ = 'sync_task'
    id = db.Column(db.Integer, primary_key=True)
    sync = relationship("Sync", back_populates="tasks")
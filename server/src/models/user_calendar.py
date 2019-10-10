from sqlalchemy.orm import relationship

from models.base import Base, db


class CalendarEvents(Base):
    __tablename__ = 'calendar_events'
    __bind_key__ = 'user_db'
    id = db.Column(db.String(100), primary_key=True)
    calendar_id = db.Column(db.String(150))
    created_at = db.Column(db.TIMESTAMP)
    organizer_email = db.Column(db.String(200))
    is_recurring = db.Column(db.BOOLEAN)
    title = db.Column(db.String(500))
    location = db.Column(db.String(500))
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    description = db.Column(db.String(5000))
    calendar_event_attendees = relationship("CalendarEventAttendees", back_populates="calendar_event")


class CalendarEventAttendees(Base):
    __tablename__ = 'calendar_event_attendees'
    __bind_key__ = 'user_db'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(100), db.ForeignKey('calendar_events.id'))
    email = db.Column(db.String(200))
    working_hours_start_time = db.Column(db.TIME)
    working_hours_end_time = db.Column(db.TIME)
    display_name = db.Column(db.String(200))
    response_status = db.Column(db.String(20))
    is_organizer = db.Column(db.BOOLEAN)
    is_optional = db.Column(db.BOOLEAN)
    calendar_event = relationship("CalendarEvents", back_populates="calendar_event_attendees")

import time

from flask_login import login_required, current_user
from flask import Blueprint, session, request
from sqlalchemy import create_engine


from utils.app import jsonify, app
from utils.tasks import create_task
from data.api_credentials import get_calendar_api_client
from models.base import db
from models.app_main import User
from models.user_calendar import CalendarEvents, CalendarEventAttendees, CalendarUser, CalendarUserAlias

from sqlalchemy.orm import sessionmaker


syncs = Blueprint('syncs', __name__)

CALENDAR_SYNC_HANDLER_URL = '/api/syncs/tasks/calendar_sync'

# TODO Store and use synctokens

@syncs.route('/api/syncs/')
@login_required
def list_syncs():
    return jsonify([])


@syncs.route('/api/syncs', methods=['POST'])
@login_required
def configure_sync():
    user_id = current_user.id
    data = request.json
    print(data)
    sync_type = data['sync_type'] or 'google_calendar'
    synced_ids = data['synced_ids']

    create_task(request, CALENDAR_SYNC_HANDLER_URL, {
        "user_id": user_id,
        "calendars": synced_ids
    })
    return jsonify(data)


def update_task_status():
    pass


def store_event_data(calendar_id, data, database_session):
    objects = []

    # for event in data:
    #     e = event
    #     print("EVENT")
    #     db_event = CalendarEvents(
    #         calendar_id=calendar_id,
    #         created_at=e.created,
    #         organizer_email=e.organizer.email,
    #         is_recurring=not not e.recurringEventId,
    #         title=e.summary,
    #         location=e.location,
    #         # TODO change format, add function for conversion
    #         start_time=e.start,
    #         # TODO change format, add function for conversion
    #         end_time=e.start,
    #         description=e.description
    #     )
    #     objects.append(db_event)
    #     for attendee in event.get('attendees'):
    #         db_attendee = CalendarEventAttendees(
    #             calendar_event=db_event
    #         )
    #         objects.append(db_attendee)
    #         print(attendee)

    database_session.bulk_save_objects(objects)
    # database_session.commit()


@syncs.route(CALENDAR_SYNC_HANDLER_URL, methods=['POST'])
def task_calendar_sync():
    # Getting the details about the sync job
    data = request.json
    user_id = data['user_id']
    calendars = data['calendars']

    # Get the API client
    cal_client = get_calendar_api_client(user_id)

    user = User.query.get(int(user_id))

    # TODO this is assuming the user always has one database, which is true for now
    database = user.databases[0]
    database_url = database.get_url()
    engine = create_engine(database_url)
    database_session = sessionmaker(bind=engine)

    # Loop through all the calendars we need to fetch
    for cal in calendars:
        all_events = []
        response = cal_client.events().list(calendarId=cal,
                                            maxResults=100,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        nextPageToken = response.get('nextPageToken')
        events = response.get('items', [])
        
        all_events = events

        while nextPageToken:
            # Fetch this series of results
            response = cal_client.events().list(
                                            calendarId=cal,
                                            maxResults=100,
                                            singleEvents=True,
                                            orderBy='startTime',
                                            pageToken=nextPageToken).execute()
            nextPageToken = response.get('nextPageToken')
            events = response.get('items', [])
            all_events = all_events + events

        store_event_data(cal, all_events, database_session)

    print("Start sleep")
    time.sleep(5)
    print("End sleep sleep")
    return jsonify({
        "DONE": True
    })

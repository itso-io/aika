import time
from pprint import pprint

from flask_login import login_required
from flask import Blueprint, session, request
from sqlalchemy import create_engine
import dateutil.parser
import logging
from datetime import datetime, timedelta
import pytz

from utils.app import jsonify, app, get_nested
from utils.tasks import create_task
from data.api_credentials import get_calendar_api_client, get_user_api_client
from models.base import db
from models.app_main import User
from models.user_calendar import CalendarEvents, CalendarEventAttendees, CalendarUser, CalendarUserAlias

from sqlalchemy.orm import sessionmaker

# TODO do 31 days for now, to make sure things go fast and we don't get into trouble with gcal limits
HISTORIC_DAYS_TO_PULL = 31
FUTURE_DAYS_TO_PULL = 31

CALENDAR_SYNC_HANDLER_URL = '/api/syncs/tasks/calendar_sync'


def update_task_status():
    pass

def store_calendar_event_attendees(event, attendee, email, database_session, is_organizer):
    event_id = event.get('id')
    attendee_primary_key = (event_id, email)
    calendar_user_alias = database_session.query(CalendarUserAlias).get(email)

    attendee_values = {
        'event_id': event_id,
        'invited_email': email,
        'is_organizer': is_organizer
    }


    if attendee:
        attendee_values['is_optional'] = bool(attendee.get('optional'))
        if attendee.get('displayName'):
            attendee_values['display_name'] = attendee.get('displayName')
        elif calendar_user_alias:
            attendee_values['display_name'] = calendar_user_alias.calendar_user.full_name
        attendee_values['response_status'] = attendee.get('responseStatus')
        attendee_values['is_organizer'] = bool(attendee.get('organizer'))
        attendee_values['comment'] = attendee.get('comment')
    else:
        #TODO assume that the user is the organizer of the event and the only attendee, so not optional
        attendee_values['is_optional'] = False
        attendee_values['is_organizer'] = True
        if calendar_user_alias:
            attendee_values['display_name'] = calendar_user_alias.calendar_user.full_name
        else: 
            attendee_values['display_name'] = email
        attendee_values['response_status'] = 'accepted'
        
        attendee_values['comment'] = ''


    if calendar_user_alias:
        attendee_values['calendar_user_id'] = calendar_user_alias.calendar_user.id

    calendar_event_attendee = insert_or_update(CalendarEventAttendees, attendee_primary_key, attendee_values, database_session)

def store_calendar_events(calendar_id, data, database_session):
    for event in data:
        primary_key = event.get('id')
        values = {
            "event_id": primary_key,
            "created_at": dateutil.parser.parse(event.get('created')),
            "updated_at": dateutil.parser.parse(event.get('updated')),
            "organizer_email": get_nested(event, 'organizer', 'email'),
            "creator_email": get_nested(event, 'creator', 'email'),
            "status": event.get('status'),
            "is_recurring": not not event.get('recurringEventId'),
            "recurrence_id": event.get('recurringEventId'),
            "title": event.get('summary'),
            "location": event.get('location'),
            "description": event.get('description')
        }
        if get_nested(event, 'start', 'dateTime'):
            values['start_time'] = dateutil.parser.parse(get_nested(event, 'start', 'dateTime'))

        if get_nested(event, 'end', 'dateTime'):
            values["end_time"] = dateutil.parser.parse(get_nested(event, 'end', 'dateTime'))

        is_organizer = get_nested(event, 'organizer', 'self')

        calendar_event = insert_or_update(CalendarEvents, primary_key, values, database_session)
        if event.get('attendees') is None and is_organizer:
            store_calendar_event_attendees(
                event,
                None,
                calendar_id,
                database_session,
                is_organizer
            )
        else:
            for attendee in event.get('attendees') or []:
                attendee_primary_key = (event.get('id'), attendee.get('email'))
                store_calendar_event_attendees(
                    event,
                    attendee,
                    attendee.get('email'),
                    database_session,
                    is_organizer
                )

    database_session.commit()



def get_calendar_events(cal_client, cal):
    # Loop through all the calendars we need to fetch
    start_datetime = datetime.utcnow() - timedelta(days=HISTORIC_DAYS_TO_PULL)
    start_datetime = start_datetime.replace(tzinfo=pytz.UTC)

    end_datetime = datetime.utcnow() + timedelta(days=FUTURE_DAYS_TO_PULL)
    end_datetime = end_datetime.replace(tzinfo=pytz.UTC)

    logging.info(f'Getting calendar data for {cal} from {start_datetime} - {end_datetime}')

    try:
        all_events = []
        response = cal_client.events().list(calendarId=cal,
                                            maxResults=100,
                                            singleEvents=True,
                                            orderBy='startTime',
                                            timeMin=start_datetime.isoformat(),
                                            timeMax=end_datetime.isoformat(),
                                            timeZone='UTC').execute()
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
                timeMin=start_datetime.isoformat(),
                timeMax=end_datetime.isoformat(),
                pageToken=nextPageToken).execute()
            nextPageToken = response.get('nextPageToken')
            events = response.get('items', [])
            all_events = all_events + events
    except Exception as err:
        print(err)
        raise err
    return all_events


def set_object_values(obj, values):
    for key, val in values.items():
        setattr(obj, key, val)


def insert_or_update(obj_type, primary_key, values, session):
    obj = session.query(obj_type).get(primary_key)
    if obj:
        set_object_values(obj, values)
    else:
        obj = obj_type()
        set_object_values(obj, values)
        session.add(obj)
    return obj


# TODO I think this can be done more efficient but didn't get it to work fast enough. See https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.bulk_save_objects
def store_calendar_users(users, database_session):
    obs = []
    for user in users:
        primary_key = user.get('id')
        values = {
          'id': user.get('id'),
          'primary_alias': user.get('primaryEmail'),
          'given_name': get_nested(user, 'name', 'givenName'),
          'family_name': get_nested(user, 'name', 'familyName'),
          'full_name': get_nested(user, 'name', 'fullName'),
          'current_calendar_timezone': user.get('timezone')
        }
        calendar_user = insert_or_update(CalendarUser, primary_key, values, database_session)
        if user.get('emails'):
            for email in user.get('emails'):
                primary_key = email.get('address')
                values = {
                    'alias': primary_key,
                    'calendar_user': calendar_user,
                    'calendar_user_id': calendar_user.id
                }
                insert_or_update(CalendarUserAlias, primary_key, values, database_session)
        else:
            primary_key = user.get('primaryEmail')
            values = {
                'alias': user.get('primaryEmail'),
                'calendar_user': calendar_user,
                'calendar_user_id': calendar_user.id
            }
            insert_or_update(CalendarUserAlias, primary_key, values, database_session)

    database_session.commit()


def get_calendar_users(user, calendars, cal_client):
    user_client = get_user_api_client(user.id)

    # TODO is this the best way to get the domain or customer ID for a user?
    domain = user.email[user.email.find("@") + 1:]
    page_token = None
    users = []
    i = 0
    while True:
        if domain == 'gmail.com':
            user_list = None
            page_users = [{
                'id': user.sub, # sub
                'primaryEmail': user.email,
                'name': {
                    'givenName': user.given_name,
                    'familyName': user.family_name,
                    'fullName': user.name
                }
            }]
        else:
            user_list = user_client.users().list(
                pageToken=page_token, 
                viewType='domain_public', domain=domain).execute()
            page_users = user_list.get('users', [])
        for entry in page_users:
            if entry['primaryEmail'] in calendars:
                request = cal_client.calendars().get(calendarId=entry['primaryEmail']).execute()
                if i == 0:
                    i = 1
                entry['timezone'] = request.get('timeZone')

                users.append(entry)
        if user_list:
            page_token = user_list.get('nextPageToken')
        if not page_token:
            break
    return users


def calendar_sync_main(user_id, calendars):
    # Get the API client
    user = User.query.get(int(user_id))

    # TODO this is assuming the user always has one database, which is true for now
    database = user.databases[0]
    database_url = database.get_url()
    engine = create_engine(database_url)
    database_session = sessionmaker(bind=engine)()

    cal_client = get_calendar_api_client(user.id)

    users = get_calendar_users(user, calendars, cal_client)
    store_calendar_users(users, database_session)

    for cal in calendars:
        cal_events = get_calendar_events(cal_client, cal)
        store_calendar_events(cal, cal_events, database_session)

    database_session.close()

    return {
        "DONE": True
    }


def start_calendar_sync_task(req, calendar_sync_settings):
    user_id = calendar_sync_settings.user_id
    calendars = calendar_sync_settings.synced_calendars

    create_task(req, CALENDAR_SYNC_HANDLER_URL, {
        "user_id": user_id,
        "calendars": calendars
    })

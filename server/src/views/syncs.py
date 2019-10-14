import time

from flask import Blueprint, session, request
from utils.app import jsonify, app
from utils.tasks import create_task
from data.api_credentials import get_calendar_api_client


syncs = Blueprint('syncs', __name__)

CALENDAR_SYNC_HANDLER_URL = '/tasks/calendar_sync'

@syncs.route('/api/syncs/<int:user_id>')
def get_sync():
    return jsonify({
        'status': 'syncing',
        'synced_calendars': [
            'jon@itso.io',
            'lucas@itso.io'
        ]
    })


@syncs.route('/api/syncs/')
def list_syncs():
    return jsonify([])


@syncs.route('/api/syncs', methods=['POST'])
def configure_sync():
    data = request.json
    email = session['user_email'] if 'user_email' in session else 'lucas@itso.io'
    print(data)
    sync_type = data['sync_type'] or 'google_calendar'
    synced_ids = data['synced_ids']

    create_task(request, CALENDAR_SYNC_HANDLER_URL, {
        "food": "burger",
        "email": email,
        "calendars": synced_ids
    })
    return jsonify(data)


@syncs.route(CALENDAR_SYNC_HANDLER_URL, methods=['POST'])
def task_calendar_sync():
    print("Body:")
    data = request.json
    print(data)
    email = data['email']
    calendars = [email]  # data['calendars']

    cal_client = get_calendar_api_client(email)
    print('et')

    for cal in calendars:
        events_result = cal_client.events().list(calendarId=cal,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


    print("Start sleep")
    time.sleep(5)
    print("End sleep sleep")
    return jsonify({
        "DONE": True
    })

import time

from flask import Blueprint, session, request
from utils.app import jsonify, app
from utils.tasks import add_task


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
    print(data)
    database_id = data['database_id']
    sync_type = data['sync_type'] or 'google_calendar'
    synced_ids = data['synced_ids']

    add_task(request, CALENDAR_SYNC_HANDLER_URL)
    return jsonify(data)


@syncs.route(CALENDAR_SYNC_HANDLER_URL)
def task_calendar_sync():
    print("Start sleep")
    time.sleep(5)
    print("End sleep sleep")
    return jsonify({
        "DONE": True
    })

import time

from flask import Blueprint, session, request
from utils.app import jsonify, app
from utils.tasks import add_task

syncs = Blueprint('syncs', __name__)


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
    
    add_task()
    return jsonify(data)


@syncs.route('/tasks/calendar_sync')
def task_calendar_sync():
    for key, val in app.config.items():
        print(key, val)
    print("Start sleep")
    time.sleep(20)
    print("End sleep sleep")
    return jsonify({
        "DONE": True
    })


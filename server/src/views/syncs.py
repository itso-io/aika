import time


from flask_login import login_required, current_user
from flask import Blueprint, session, request
from utils.app import jsonify, app
from utils.tasks import create_task
from data.api_credentials import get_calendar_api_client


syncs = Blueprint('syncs', __name__)

CALENDAR_SYNC_HANDLER_URL = '/api/syncs/tasks/calendar_sync'

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


@syncs.route(CALENDAR_SYNC_HANDLER_URL, methods=['POST'])
def task_calendar_sync():
    print("Body:")


    data = request.json
    user_id = data['user_id']
    calendars = data['calendars']
    print('et')
    cal_client = get_calendar_api_client(user_id)
    print('et')



    print("Start sleep")
    time.sleep(5)
    print("End sleep sleep")
    return jsonify({
        "DONE": True
    })

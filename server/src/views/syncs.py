import time

from flask_login import login_required, current_user
from flask import Blueprint, session, request
from sqlalchemy import create_engine


from utils.app import jsonify, app
from utils.tasks import create_task
from data.api_credentials import get_calendar_api_client, get_user_api_client
from models.base import db
from models.app_main import User
from models.user_calendar import CalendarEvents, CalendarEventAttendees, CalendarUser, CalendarUserAlias
from controllers.syncs import calendar_sync_main

from sqlalchemy.orm import sessionmaker


syncs = Blueprint('syncs', __name__)

CALENDAR_SYNC_HANDLER_URL = '/api/syncs/tasks/calendar_sync'

# TODO Store and use synctokens


@syncs.route('/api/syncs/')
@login_required
def list_syncs():
    return jsonify([])


@syncs.route('/api/syncs', methods=['POST'])
def create_sync():
    user_id = current_user.id
    data = request.json
    sync_type = data.get('sync_type') or 'google_calendar'
    synced_ids = data['synced_ids']

    if sync_type == 'google_calendar':
        create_task(request, CALENDAR_SYNC_HANDLER_URL, {
            "user_id": user_id,
            "calendars": synced_ids
        })
    data['user_id'] = current_user.id
    return jsonify(data)


@syncs.route(CALENDAR_SYNC_HANDLER_URL, methods=['POST'])
def task_calendar_sync():
    # Getting the details about the sync job
    data = request.json
    user_id = data['user_id']
    calendars = data['calendars']

    result = calendar_sync_main(user_id, calendars)

    # Testing the async tasks
    print("Start sleep")
    time.sleep(5)
    print("End sleep sleep")

    return jsonify(result)

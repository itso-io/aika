from flask import Blueprint, session, request, jsonify
from flask_login import login_required, current_user

from data.api_credentials import get_calendar_api_client

calendars = Blueprint('calendars', __name__)


def _is_relevant_calendar(calendar_id, user_email):
  # filters out calendars like `en.usa#holiday@group.v.calendar.google.com` (US Holiday calendars) and
  # `addressbook#contacts@group.v.calendar.google.com` (Contacts).
  #
  # Relevant calendar examples:
  # - {"id": "itsotester3@gmail.com", "summary": "itsotester3@gmail.com"}
  # - {"id": "6e6hrodgbluct03bq6h62sdbf8@group.calendar.google.com", "summary": "My Second Calendar"}
  # - {"id": "itso.io_achdr2ab8qi9hmado0legi54bk@group.calendar.google.com", "summary": "Jon's Second Calendar"}
  # - {"id": "jon@itso.io", "summary": "jon@itso.io"}

  if calendar_id == user_email:
    return True

  if calendar_id.endswith('@group.calendar.google.com'):
    return True

  user_domain = user_email.split('@')[1]

  if user_domain == 'gmail.com':
    return False

  return calendar_id.startswith('%s_' % (user_domain)) or calendar_id.endswith('@%s' % (user_domain))


@calendars.route('/api/calendars')
@login_required
def get_calendars():
  cal_client = get_calendar_api_client(current_user.id)

  calendars = []
  page_token = None
  while True:
    calendar_list = cal_client.calendarList().list(pageToken=page_token).execute()
    calendars.extend([{'id': entry['id'],
                       'summary': entry['summary']}
                      for entry in calendar_list['items']
                      if _is_relevant_calendar(entry['id'], current_user.email)])
    page_token = calendar_list.get('nextPageToken')
    if not page_token:
      break

  return jsonify(calendars)

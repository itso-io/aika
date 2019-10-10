from flask import Blueprint, session, render_template, abort, redirect, request, url_for, jsonify
import google_auth_oauthlib.flow
import jwt

from data import api_credentials
from utils.common import get_file_full_path


CLIENT_SECRETS_FILE = get_file_full_path('google_client_secret.json')
REQUIRED_SCOPES = ['openid',
                   'https://www.googleapis.com/auth/userinfo.email',
                   'https://www.googleapis.com/auth/calendar.readonly']

auth = Blueprint('auth', __name__)


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'scopes': credentials.scopes}


@auth.route('/auth/google/init')
def auth_init():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                                                   REQUIRED_SCOPES)

    flow.redirect_uri = url_for('auth.auth_callback', _external=True)

    authorization_url, state = flow.authorization_url(access_type='offline',
                                                      include_granted_scopes='true')

    session['state'] = state

    return redirect(authorization_url)


@auth.route('/auth/google/callback')
def auth_callback():
    if request.args.get('error') == 'access_denied':
        return redirect('/')

    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                                                   scopes=REQUIRED_SCOPES,
                                                                   state=state)

    flow.redirect_uri = url_for('auth.auth_callback', _external=True)

    flow.fetch_token(authorization_response=request.url)

    # this token came from Google, so don't worry aboue re-verifying its signature in this context
    id_data = jwt.decode(flow.credentials.id_token, verify=False)

    session['user_email'] = None if not id_data['email_verified'] else id_data['email']

    # refresh token only provided on initial auth
    if session['user_email'] and flow.credentials.refresh_token:
        api_credentials.store_user_api_credentials(
            session['user_email'], flow.credentials)

    return redirect('/database')


@auth.route('/auth/google/check')
def auth_check():
    # See https://developers.google.com/calendar/quickstart/python
    calendar_client = api_credentials.get_calendar_api_client(
        session['user_email'])

    events_result = calendar_client.events().list(calendarId='primary',
                                                  maxResults=10,
                                                  singleEvents=True,
                                                  orderBy='startTime'
                                                  ).execute()

    events = events_result.get('items', [])

    return jsonify(events)

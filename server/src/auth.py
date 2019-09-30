from flask import Blueprint, session, render_template, abort, redirect, request, url_for
import google_auth_oauthlib.flow
import jwt

from utils import get_file_full_path


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
  state = session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                                                 scopes=REQUIRED_SCOPES,
                                                                 state=state)

  flow.redirect_uri = url_for('auth.auth_callback', _external=True)

  flow.fetch_token(authorization_response=request.url)

  # TODO: Store these credentials with the user's email
  credentials = flow.credentials
  session['credentials'] = credentials_to_dict(credentials)

  # this token came from Google, so don't worry aboue re-verifying its signature in this context
  id_data = jwt.decode(credentials.id_token, verify=False)

  session['user_email'] = None if not id_data['email_verified'] else id_data['email']

  return session['user_email']

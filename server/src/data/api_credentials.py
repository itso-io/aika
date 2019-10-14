import datetime
import pickle

from google.cloud import datastore
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


datastore_client = datastore.Client()


def store_user_api_credentials(user_id, credentials):
    entity = datastore.Entity(key=datastore_client.key('APICredentials'),
                              exclude_from_indexes=['credentials'])
    entity.update({
        'created': datetime.datetime.utcnow(),
        'user': user_id,
        'credentials': pickle.dumps(credentials)
    })

    datastore_client.put(entity)


def get_user_api_credentials(user_id):
    query = datastore_client.query(kind='APICredentials')
    query.add_filter('user', '=', user_id)
    query.order = ['-created']

    credentials = list(query.fetch(limit=1))

    if not credentials:
        return None

    return pickle.loads(credentials[0]['credentials'])


def get_calendar_api_client(user_id):
    credentials = get_user_api_credentials(user_id)

    if not credentials:
        return None

    if credentials.expired:
        credentials.refresh(Request())

    return build('calendar', 'v3', credentials=credentials)

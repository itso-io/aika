import threading
import requests
import os
from utils.app import app
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2


def start_local_task(url):
    print(url)
    requests.get(url)


def add_task(req, relative_url):
    print('Start add task function')
    if not os.getenv('GOOGLE_CLOUD_PROJECT'):
        url = f'{req.scheme}://{req.host}{relative_url}'
        print(url)
        x = threading.Thread(target=start_local_task, daemon=True, args=[url])
        x.start()
    else:
        client = tasks_v2.CloudTasksClient()
        project = os.getenv('GOOGLE_CLOUD_PROJECT')
        queue = app.config['CLOUD_TASK_QUEUE']
        location = 'us-central1'
        payload = '{ "data": "hello" }'

        parent = client.queue_path(project, location, queue)

        task = {
                'app_engine_http_request': {  # Specify the type of request.
                    'http_method': 'POST',
                    'relative_uri': relative_url
                }
        }
        if payload is not None:
            # The API expects a payload of type bytes.
            converted_payload = payload.encode()

            # Add the payload to the request.
            task['app_engine_http_request']['body'] = converted_payload

        response = client.create_task(parent, task)

        print('Created task {}'.format(response.name))

    print('End add task function')

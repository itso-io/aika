import threading
import requests

from utils.app import app


def start_local_task():
    url = 'http://localhost:5000/tasks/calendar_sync'
    requests.get(url)


def add_task():
    print('Start add task function')
    # x = threading.Thread(target=start_local_task, daemon=True)
    # x.start()
    print('End add task function')

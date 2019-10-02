import os

from utils import set_logging, set_config
from flask import Flask
from auth import auth
import logging



app = Flask(__name__)
set_logging(app)
set_config(app)


@app.route('/')
def hello():
    return 'Hello World!'


app.register_blueprint(auth)


if __name__ == '__main__':
    # TODO: Set debug=false if not running locally
    app.run(host='localhost', port=5000, debug=True)

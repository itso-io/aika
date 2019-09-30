import os

from flask import Flask

from auth import auth


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')


@app.route('/')
def hello():
    return 'Hello World!'


app.register_blueprint(auth)


if __name__ == '__main__':
    # TODO: Set debug=false if not running locally
    app.run(host='localhost', port=5000, debug=True)

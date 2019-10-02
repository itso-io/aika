from models.shared import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    test = db.Column(db.String(128))
    test_2 = db.Column(db.String(128))

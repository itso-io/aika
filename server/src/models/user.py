from models.shared import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    nickname = db.Column(db.String(128))

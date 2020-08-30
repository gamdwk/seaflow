from ..models import db


class Games(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    images = db.Column(db.String, unique=True)

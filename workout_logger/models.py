from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(100), unique=True)
    password=db.Column(db.String(100))
    name=db.Column(db.String(100))
    workouts=db.relationship('Workouts', backref='user',lazy=True)

class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name=db.Column(db.String(100), nullable=False)
    sets=db.Column(db.Integer, nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

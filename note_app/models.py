from sqlalchemy_utils import URLType
from note_app import db 
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from sqlalchemy.orm import backref

class Note(db.Model):
    """Note Model"""
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='notes')
    created_by = db.relationship('User')

class Reminder(db.Model):
    """Reminder Model"""
    content = db.Column(db.String(200), nullable=False)
    alert_date = db.Column(db.datetime)
    category = db.Column(db.String(200), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'  
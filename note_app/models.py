from sqlalchemy_utils import URLType
from note_app import db 
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from sqlalchemy.orm import backref
from flask_login import UserMixin

class Note(db.Model):
    """Note Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(200), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='notes')
    created_by = db.relationship('User')

class Reminder(db.Model):
    """Reminder Model"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    alert_date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(200), nullable=False)
    user = db.relationship('User', back_populates='reminders')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    notes = db.relationship('Note', back_populates='user')
    reminders = db.relationship('Reminder', back_populates='user')
    def __repr__(self):
        return f'<User: {self.username}>'  
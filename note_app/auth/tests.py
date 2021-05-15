#!/usr/bin/env python3
import os
import unittest

from datetime import date
 
from note_app import app, db, bcrypt
from note_app.models import Note, Reminder, User

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

class AuthTests(unittest.TestCase):

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all() 

    def test_signup(self):
        post_data = {
            'username': 'test1',
            'password': '1246',
        }
        self.app.post('/signup', data=post_data)
        self.assertEqual("test", user.username)
        user = User.query.filter_by(username='test1').one_or_none()
        self.assertIsNotNone(user)
    
       
    def test_login_correct_password(self):
        # Test for the login route. It should
        #Create a user
        create_user()

        post_data = {
            'username': 'me1',
            'password': 'password',
        }
        self.app.post('/signup', data=post_data)

        response = self.app.get('/login', data=post_data, follow_redirects=True)

        response_text = response.get_data(as_text=True)
        self.assertNotIn("Log In", response_text)
        self.assertIn("me1", response_text)
     
    def test_logout(self):
    
        create_user()
     
        post_data = {
            'username': 'mee',
            'password': 'password',
        }
        self.app.post('/login', data=post_data)

        self.app.get('/logout', data=post_data)

        response = self.app.get('/', follow_redirects=True)
        
        response_text = response.get_data(as_text=True)
        self.assertNotIn('Log Out', response_text)

    def test_login_nonexistent_user(self):
        post_data = {
            'username': 'test2',
            'password': 'password',
        }
        response = app.test_client().post('/login', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertNotIn("Log Out", response_text)
        self.assertIn('test2', response_text)
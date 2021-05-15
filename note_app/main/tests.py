import os
import unittest

from datetime import date
 
from note_app import app, db, bcrypt
from note_app.models import Note, Reminder, User

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_user():
    password_hash = bcrypt.generate_password_hash('soup').decode('utf-8')
    user = User(username='4me', password=password_hash)
    db.session.add(user)
    db.session.commit()

def create_note():
    n1 = Note(
        title='Groceries',
        body='eggs',
    )
    db.session.add(n1)
    db.session.commit()

def create_reminder():
    r1 = Reminder(
        content='Pickup ham',
        alert_date=2021-12-18,
        category='Errands',
    )
    db.session.add(r1)
    db.session.commit()


class MainTests(unittest.TestCase):

      def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

      def test_homepage_logged_in(self):
        """Test that the notes show up on the homepage."""
        # Set up
        create_note()
        create_user()
        login(self.app, 'peac3', 'popcorn')

        # Makes a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Checks that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Groceries', response_text)
        self.assertIn('eggs', response_text)
        self.assertIn('peac3', response_text)
        self.assertIn('Create Note', response_text)
        self.assertIn('Create Reminder', response_text)
      

        # Checks that the page doesn't contain things we don't expect
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    
      def test_create_note(self):
        # Set up
        create_note()
        create_user()
        login(self.app, 'peac3', 'popcorn')

        # Makes POST request with data
        post_data = {
            'title': 'Todo List',
            'body': 'Relax',
        }
        self.app.post('/create_note', data=post_data)

        # Makes sure note was updated as we'd expect
        created_note = Note.query.filter_by(title='Todo List').one_or_none()
        self.assertIsNotNone(created_note)
        self.assertEqual(created_note.title, "Todo List")
    
      def test_create_reminder(self):
        create_reminder()
        create_user()
        login(self.app, 'peace3', 'popcorn')

        post_data = {
            'content': 'Hire plumber',
            'alert_date': '2021-05-18',
            'category': 'Household',
        }
        self.app.post('/create_reminder', data=post_data)

        # Checks to confirm reminder setup
        created_reminder = Reminder.query.filter_by(content='Hire plumber').one_or_none()
        self.assertIsNotNone(created_reminder)
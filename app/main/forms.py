from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, TextAreaField, SubmitField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from app.models import Note, Reminder, User

class NoteForm(FlaskForm):
    title = StringField('Note Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    body = TextAreaField('Body')
    submit = SubmitField('Submit')

class ReminderForm(FlaskForm):
    """Form to create a book."""
    content = StringField('Content',
        validators=[DataRequired(), Length(min=3, max=80)])
    alert_date = DateField('Alert Date')
    category = StringField('Category')
    submit = SubmitField('Submit')
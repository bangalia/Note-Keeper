from note_app.main.forms import NoteForm, ReminderForm
from note_app.models import Note, Reminder
from flask import Blueprint, render_template, redirect, url_for, flash
from note_app import bcrypt
from flask_login import login_user, logout_user, login_required, current_user 

from note_app import app, db

main = Blueprint('main', __name__)

@main.route('/')
def homepage():
    all_notes = Note.query.all()
    print(all_notes)
    return render_template('base.html', all_notes=all_notes)

@main.route('/new_note', methods=['GET', 'POST'])
@login_required
def new_note():
    #Creates a Note Form
    form= NoteForm()

    if form.validate_on_submit():
        new_note = Note(
            title=form.title.data,
            body=form.body.data,
        )
        db.session.add(new_note)
        db.session.commit()

        flash('New Note was created successfully!')
        return redirect(url_for('new_note'))
    return render_template('new_note.html')

@main.route('/new_reminder', methods=['GET', 'POST'])
@login_required
def new_reminder():
    #Creates a Reminder Form
    form= ReminderForm()

    if form.validate_on_submit():
        new_reminder = Reminder(
            content=form.content.data,
            alert_date=form.alert_date.data,
            category=form.category.data
        )
        db.session.add(new_reminder)
        db.session.commit()

        flash('New reminder was saved successfully!')
        return redirect(url_for('reminder'))
    
    return render_template('new_reminder.html')

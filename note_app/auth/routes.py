from flask import Blueprint, request, render_template, redirect, url_for, flash
from note_app.auth.forms import SignUpForm, LoginForm
from note_app.models import Note, Reminder, User
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from note_app import bcrypt

from note_app import app, db


auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)
#Routes here.

@main.route('/')
def homepage():
    all_notes = Note.query.all()
    all_reminders = Reminder.query.all()
    print(all_notes)
    return render_template('home.html', all_notes=all_notes, all_reminders=all_reminders)
    

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.arg.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('home.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

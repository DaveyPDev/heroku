from flask import Flask, render_template, redirect, session, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from werkzeug.exceptions import Unauthorized
from forms import LoginForm, RegisterForm, FeedbackForm, DeleteForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_auth_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404


@app.route('/')
def home_page():

    return redirect('/register')


@app.route('/register', methods=["GET", "POST"])
def register_user():
    if 'username' in session: 
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username

        
        return redirect('/login')

    return render_template('/users/register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():

    if 'username' is session: 
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']
            return render_template('users/login.html', form=form)
        
    return render_template('users/login.html', form=form)


@app.route('/users/<username>')
def user_info(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template('users/show.html', user=user, form=form)


@app.route('/logout')
def logout():
    session.pop('username')
    flash('Goodbye!', 'info')
    return redirect('/login')


@app.route('/users/<username>/delete', methods=["GET", "POST"])
def delete_user(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')

    return redirect('/login')


@app.route('/users/<username>/feedback/new', methods=["GET", "POST"])
def feedback_add(username):

    if 'username' not in session or username != session['username']:
     raise Unauthorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title = title,
            content = content,
            username = username
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template('feedback/new.html', form=form)

# @app.route('/users/feedback/update', methods=["GET", "POST"])


@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def feedback_update(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template('/feedback/edit.html', form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=["GET", "POST"])
def feedback_delete(feedback_id):

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

        flash('Feedback deleted!', 'info')
        return redirect(f"/users/{feedback.username}")

    return render_template('feedback/delete.html', form=form, feedback=feedback)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional

class LoginForm(FlaskForm):
    ''' Login Form '''
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=30)])

class RegisterForm(FlaskForm):
    """ Register Form """
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=30)])
    email = StringField('Email', validators=[InputRequired(), Length(max=30)])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])

class FeedbackForm(FlaskForm):
    """ Feedback Form"""

    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = StringField('Content', validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """ Delete Form """


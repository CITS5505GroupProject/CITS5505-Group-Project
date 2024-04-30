from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email


class login(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Log in')

class signup(FlaskForm):
    email = StringField('Email')
    username = StringField('Username')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('register')

class createPost(FlaskForm):
    title = StringField('Title')
    desc = StringField('Description')
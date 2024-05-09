from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, FieldList, FormField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# User login
class loginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    submit = SubmitField('Login')

# User registration
class registrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Register')

# Create a survey with multiple questions, and each question with multiple options
class questionOptionForm(FlaskForm):
    text = StringField('OptionText', validators=[DataRequired()])

class surveyQuestionForm(FlaskForm):
    text = StringField('QuestionText', validators=[DataRequired()])
    options = FieldList(FormField(questionOptionForm), min_entries=2, max_entries=10)

class createSurveyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    questions = FieldList(FormField(surveyQuestionForm), min_entries=1, max_entries=10)
    submit = SubmitField('Create')

# Update User profile
class updateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_pic = FileField('Update Profile Picture')
    submit = SubmitField('Update Profile')

# Change Password
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, message='Your password must be at least 6 characters long.')
    ])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Change Password')
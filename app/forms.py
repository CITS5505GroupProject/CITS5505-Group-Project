from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileAllowed, FileField

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

# Create a survey
class createSurveyForm(FlaskForm):
    survey_types = [
        ('business', 'Business'),
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('technology', 'Technology'),
        ('entertainment', 'Entertainment'),
        ('social', 'Social'),
        ('politcs', 'Politcs'),
        ('science', 'Science'),
        ('environment', 'Environment'),
        ('personal_development', 'Personal Development')
    ]
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    surveyType = SelectField('Select a type', choices=survey_types, validators=[DataRequired()])
    submit = SubmitField('Create')

# Update User profile
class updateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
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

# Option selection
class OptionForm(FlaskForm):
    # This subform represents a single option
    choice = RadioField('Choice')

# Reset password form
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Reset Password")
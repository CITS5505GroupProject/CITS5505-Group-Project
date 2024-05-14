from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app, db, os, mail
from models import User, Survey, Question, Option, UserAnswer
from forms import registrationForm, loginForm, createSurveyForm, RadioField, SubmitField, updateProfileForm, DataRequired, FlaskForm, ResetPasswordForm, ChangePasswordForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import random
from flask_mail import Message


@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Tony', 'DoB':'10/12/2001'}
    return render_template('/index.html', title = 'Home Page', user = user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registrationForm()
    if form.validate_on_submit():
        #initial path for profile picture
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.confirm_password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists. Please use a different one.', 'danger')
    return render_template('user/register.html', title='Register', form=form)

@app.route('/dashboard')
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html', username=current_user.username)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        email = form.email.data
        pwd = form.password.data 
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(pwd):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Username or email is incorrect, try again.', 'danger')
    return render_template('user/login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/reset-password', methods = ['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data

        if User.email_exist(email):
            new_password = random.randint(10000000, 99999999)
            user = User.query.filter_by(email=email).first()
            user.set_password(str(new_password))
            db.session.commit()
            #email message
            msg = Message("Survey Stream: Reset Password", recipients=[email])
            msg.body = f"Your new password is: { new_password }. We suggest you to change this random password ASAP!."
            print(new_password)
            mail.send(msg)
            flash("A reset password has been sent to your email!", "success")
            return redirect(url_for('login'))
        else:
            flash("Email not exist. Try again...", 'danger')
        
    return render_template('user/reset_password.html', form = form)

@app.route('/change-password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.get(user_id)
        if user.check_password(form.current_password.data):
            user.set_password(form.new_password.data)
            db.session.commit()
            flash("Password changed successfully!", "success")
        else:
            flash("Current password is incorrect, try again...", "danger")
            redirect(url_for('change_password', user_id = user_id))
    return render_template('user/change_password.html', form=form)

@app.route('/create-survey', methods=['GET', 'POST'])
@login_required
def create_survey():
    survey_form = createSurveyForm()
    if survey_form.validate_on_submit():
        new_survey = Survey(title=survey_form.title.data, type=survey_form.surveyType.data, description=survey_form.description.data, creator=current_user)
        db.session.add(new_survey)
        db.session.commit()

        questions = {}
        i = 1
        while f'question{i}' in request.form:
            question_text = request.form[f'question{i}']
            new_question = Question(text=question_text, survey=new_survey)
            db.session.add(new_question)
            db.session.commit()
            options = []
            j = 1
            while f'option{i}_{j}' in request.form:
                option_text = request.form[f'option{i}_{j}']
                options.append(option_text)
                new_option = Option(text=option_text, question=new_question)
                db.session.add(new_option)
                j += 1
            questions[question_text] = options
            i += 1
        db.session.commit()
        return redirect(url_for('take_survey', survey_id = new_survey.id))

    return render_template('survey/create_survey.html', form=survey_form)

def create_survey_form(survey_id):
    class DynamicSurveyForm(FlaskForm):
        # Dynamic fields will be added here
        pass
    
    survey = Survey.query.get_or_404(survey_id)
    for question in survey.questions:
        # Create a list of tuples for the RadioField choices
        choices = [(str(option.id), option.text) for option in question.options]
        # Add a RadioField per question
        setattr(DynamicSurveyForm, 'question_' + str(question.id),
                RadioField(question.text, choices=choices, validators=[DataRequired()]))
    
    setattr(DynamicSurveyForm, 'submit', SubmitField('Submit'))
    
    return DynamicSurveyForm()

@app.route('/take-survey/<int:survey_id>', methods=['GET', 'POST'])
@login_required
def take_survey(survey_id):
    form = create_survey_form(survey_id)

    survey = Survey.query.get_or_404(survey_id)
    
    if form.validate_on_submit():
        # Handle the form submission
        # Extract answers here, e.g., form.question_1.data
        for field in form:
            print(f'{field.name} : {field.data}')
            if str(field.name).startswith("question_"):
                user_response = UserAnswer(user_id=current_user.id, option_id=field.data)
                db.session.add(user_response)
        
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    return render_template('survey/take_survey.html', form=form, survey=survey)

@app.route('/update_profile/<int:user_id>', methods=['GET', 'POST'])
def update_profile(user_id):
    if current_user.is_authenticated and current_user.id == user_id:
        user = current_user
        profile_url = user.profilePic
        form = updateProfileForm(obj=user)
        if form.validate_on_submit():
            if form.profile_pic.data:
                filename = secure_filename(form.profile_pic.data.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(filepath)
                print(filename)
                form.profile_pic.data.save(filepath)
                user.profilePic = 'user_profile/' + filename
            
            user.username = form.username.data
            db.session.commit()
            return redirect(url_for('update_profile', user_id=user_id))

    else:
        return redirect(url_for('login'))
    
    return render_template('survey/update_profile.html', form=form, profile_url=profile_url)

@app.route('/survey-dashboard')
def survey_dashboard():
    surveys = Survey.query.all()
    surveys_data = [survey.to_dict() for survey in surveys]
    return render_template('survey/survey_dashboard.html', surveys=surveys_data)
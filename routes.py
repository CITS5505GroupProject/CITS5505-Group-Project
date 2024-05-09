from flask import render_template, redirect, url_for, flash, session, request
from app import app, db
from models import User, Survey, Question, Option
from forms import registrationForm, loginForm, createSurveyForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, current_user

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

@app.route('/create-survey', methods=['GET', 'POST'])
def create_survey():
    form = createSurveyForm()
    if request.method == 'POST' and form.validate():
        # Create a new survey instance
        new_survey = Survey(title=form.title.data, description=form.description.data)
        db.session.add(new_survey)
        print("Survey added")
        # Manually parse dynamically added questions and their options
        question_count = int(request.form.get('question_count', 0))
        for i in range(question_count):
            question_text = request.form.get(f'questions[{i}][text]', '')
            if question_text:
                new_question = Question(text=question_text, survey=new_survey)
                db.session.add(new_question)
                print(f"Question {question_text} added")

                # Each question can have multiple options
                option_count = int(request.form.get(f'question_{i}_option_count', 0))
                for j in range(option_count):
                    option_text = request.form.get(f'questions[{i}][options][{j}][text]', '')
                    if option_text:
                        new_option = Option(text=option_text, question=new_question)
                        db.session.add(new_option)
                        print(f"Option {option_text} added")

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('survey/create_survey.html', form=form)

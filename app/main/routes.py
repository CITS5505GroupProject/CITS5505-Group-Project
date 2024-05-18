from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from app import db, os, mail
from app.models import User, Survey, Question, Option, UserAnswer
from app.forms import registrationForm, loginForm, createSurveyForm, RadioField, SubmitField, updateProfileForm, DataRequired, FlaskForm, ResetPasswordForm, ChangePasswordForm
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import random
from flask_mail import Message
from sqlalchemy import func
from app.main import main

@main.route('/')
@main.route('/index')
def index():
    user = {'username':'Tony', 'DoB':'10/12/2001'}
    return render_template('/index.html', title = 'Home Page', user = user)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = registrationForm()
    if form.validate_on_submit():
        #initial path for profile picture
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.confirm_password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists. Please use a different one.', 'danger')
    return render_template('user/register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        email = form.email.data
        pwd = form.password.data 
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(pwd):
            login_user(user)
            return redirect(url_for('main.update_profile', user_id = current_user.id))
        else:
            flash('Username or email is incorrect, try again.', 'danger')
    return render_template('user/login.html', title='Login', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/reset-password', methods = ['GET', 'POST'])
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
            return redirect(url_for('main.login'))
        else:
            flash("Email not exist. Try again...", 'danger')
        
    return render_template('user/reset_password.html', form = form)

@main.route('/change-password/<int:user_id>', methods=['GET', 'POST'])
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
            redirect(url_for('main.change_password', user_id = user_id))
    return render_template('user/change_password.html', form=form)

@main.route('/survey/create-survey', methods=['GET', 'POST'])
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
        current_user.point += 5
        db.session.commit()
        return redirect(url_for('main.my_survey', user_id = current_user.id))

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

@main.route('/take-survey/<int:survey_id>', methods=['GET', 'POST'])
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
                current_user.point += 2
        db.session.commit()
        return redirect(url_for('main.survey_dashboard'))
    
    return render_template('survey/take_survey.html', form=form, survey=survey)

@main.route('/update_profile/<int:user_id>', methods=['GET', 'POST'])
def update_profile(user_id):
    if current_user.is_authenticated and current_user.id == user_id:
        user = current_user
        profile_url = user.profilePic
        form = updateProfileForm(obj=user)
        if form.validate_on_submit():
            if form.profile_pic.data:
                filename = secure_filename(form.profile_pic.data.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                print(filepath)
                print(filename)
                form.profile_pic.data.save(filepath)
                user.profilePic = 'user_profile/' + filename
            
            user.username = form.username.data
            db.session.commit()
            return redirect(url_for('main.update_profile', user_id=user_id))

    else:
        return redirect(url_for('main.login'))
    
    return render_template('survey/update_profile.html', form=form, profile_url=profile_url)

@main.route('/survey-dashboard')
def survey_dashboard():
    surveys = Survey.query.all()
    surveys_data = [survey.to_dict() for survey in surveys]
    return render_template('survey/survey_dashboard.html', surveys=surveys_data)

@main.route('/my-survey/<int:user_id>', methods=['GET'])
@login_required
def my_survey(user_id):
    surveys = Survey.query.filter_by(user_id=user_id).all()
    return render_template('survey/my_surveys.html', surveys=surveys)

@main.route('/survey/delete/<int:survey_id>', methods=['DELETE', 'GET'])
@login_required
def delete_survey(survey_id):
    survey = Survey.query.get(survey_id)
    if not survey:
        return jsonify({"message": "Survey not found."}), 404

    try:
        db.session.delete(survey)
        db.session.commit()
        flash("Survey deleted successfully", "success")
        return redirect(url_for('main.my_survey', user_id=current_user.id))
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the survey.", "error": str(e)}), 500
    
@main.route('/leaderboard')
def leaderboard():
    top10 = User.query.order_by(User.point.desc()).limit(10).all()
    return render_template('ranking.html', top10 = top10)

@main.route('/about-us')
def about_us():
    return render_template('aboutus.html')

@main.route('/survey/<int:survey_id>')
def survey_result(survey_id):
    survey = Survey.query.get_or_404(survey_id)

    # Query to get questions, options, and the count of user answers for each option
    results = db.session.query(
        Question.id.label('question_id'),
        Question.text.label('question_text'),
        Option.id.label('option_id'),
        Option.text.label('option_text'),
        func.count(UserAnswer.id).label('selection_count')
    ).join(Option, Option.question_id == Question.id)\
     .outerjoin(UserAnswer, UserAnswer.option_id == Option.id)\
     .filter(Question.survey_id == survey_id)\
     .group_by(Question.id, Option.id)\
     .all()

    # Organize the data into a structured format
    survey_data = {
        'id': survey.id,
        'title': survey.title,
        'description': survey.description,
        'type': survey.type,
        'created_at': survey.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'questions': {}
    }

    for row in results:
        question_id = row.question_id
        if question_id not in survey_data['questions']:
            survey_data['questions'][question_id] = {
                'text': row.question_text,
                'options': []
            }
        survey_data['questions'][question_id]['options'].append({
            'id': row.option_id,
            'text': row.option_text,
            'selection_count': row.selection_count
        })

    return render_template('survey/survey_result.html', survey=survey_data)
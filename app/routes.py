from flask import render_template, redirect, url_for, flash, session
from app import app, db
from app.models import User
from app.forms import registrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Tony', 'DoB':'10/12/2001'}
    return render_template('index.html', title = 'Home Page', user = user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.confirm_password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            return redirect(url_for('/dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists. Please use a different one.', 'danger')
    return render_template('register.html', title = 'Register', form=form)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    return redirect(url_for('/index'))
        
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
import os
from flask_mail import Mail


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(basedir)
print(parent_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(parent_dir, 'app.db')
app.config['SECRET_KEY'] = 'you_will_not_guess'
app.config['UPLOAD_FOLDER'] = os.path.join(parent_dir, 'app/static/user_profile')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

#email setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'surveystream10@gmail.com'
app.config['MAIL_PASSWORD'] = 'gaxh zpcp gvmz mvog' #app password
app.config['MAIL_DEFAULT_SENDER'] = 'surveystream10@gmail.com'

mail = Mail(app)
csrf=CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

import models, routes

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
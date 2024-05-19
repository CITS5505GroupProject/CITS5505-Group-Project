import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_mail import Mail

# initialize
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()

# Testing config
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "TESTING_KEY"


# create app
def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        basedir = os.path.abspath(os.path.dirname(__file__))
        parent_dir = os.path.dirname(basedir)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(parent_dir, 'app.db')
        app.config['SECRET_KEY'] = 'DEPLOY_KEY'
    else:
        app.config.from_object(TestConfig)


    basedir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(basedir)
    app.config['UPLOAD_FOLDER'] = os.path.join(parent_dir, 'app/static/user_profile')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

    # Email setup
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'surveystream10@gmail.com'
    app.config['MAIL_PASSWORD'] = 'gaxh zpcp gvmz mvog'  # App password
    app.config['MAIL_DEFAULT_SENDER'] = 'surveystream10@gmail.com'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'main.login'

    with app.app_context():
        from . import models
        models.db.create_all()

        from app.main import main as main_blueprint
        app.register_blueprint(main_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app

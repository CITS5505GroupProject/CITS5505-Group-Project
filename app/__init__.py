from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(basedir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(parent_dir, 'app.db')
app.config['SECRET_KEY'] = 'you_will_not_guess'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models, routes
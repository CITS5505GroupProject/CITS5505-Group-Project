from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app import db
from flask_login import UserMixin

# calculate perth time for survey
def get_perth_time():
    return datetime.now() + timedelta(hours=8)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    profilePic = db.Column(db.String(255), default="user_profile/user_default.png") #path to save the file
    surveys = db.relationship('Survey', backref='creator', cascade="all, delete-orphan")
    point = db.Column(db.Integer, default=0, nullable=False)
    user_answers = db.relationship('UserAnswer', backref='answered', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def email_exist(email):
        user = User.query.filter_by(email=email).first()
        return user is not None
    
    def to_dict(self):
        return {
            'username': self.username,
            'profilePic': self.profilePic
        }

    def __repr__(self):
        return f'<User {self.username}>'

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=get_perth_time(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    questions = db.relationship('Question', backref='survey', cascade="all, delete-orphan")

    def to_dict(self):
        """Converts this Survey object into a dictionary format, which can be easily turned into JSON."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'type': self.type,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id,
            'creator': self.creator.to_dict() if self.creator else None,  # Assuming a backref 'creator' from User
            'questions': [question.to_dict() for question in self.questions]  # This will include questions if needed
    }

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id', ondelete='CASCADE'), nullable=False)
    options = db.relationship('Option', backref='question', cascade="all, delete-orphan")
    def to_dict(self):
        """Converts this Survey object into a dictionary format, which can be easily turned into JSON."""
        return {
            'id': self.id,
            'text': self.text,
            'options': [option.to_dict() for option in self.options]
        }

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    user_answers = db.relationship('UserAnswer', backref='selected', cascade="all, delete-orphan")
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text
        }

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id', ondelete='CASCADE'), nullable=False)

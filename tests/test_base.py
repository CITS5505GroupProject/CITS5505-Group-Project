import unittest
from app import create_app, db
from app.models import User, Survey, Question, Option, UserAnswer

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='TESTING')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # insert some mock data
        self.insert_mock_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def insert_mock_data(self):
        # Create users
        user1 = User(username='testuser1', email='testuser1@example.com')
        user1.set_password('password')
        user2 = User(username='testuser2', email='testuser2@example.com')
        user2.set_password('password')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Create surveys
        survey1 = Survey(title='Survey 1', description='First survey', type='Type A', user_id=user1.id)
        survey2 = Survey(title='Survey 2', description='Second survey', type='Type B', user_id=user2.id)
        db.session.add(survey1)
        db.session.add(survey2)
        db.session.commit()

        # Create questions
        question1 = Question(text='Question 1', survey_id=survey1.id)
        question2 = Question(text='Question 2', survey_id=survey1.id)
        question3 = Question(text='Question 1', survey_id=survey2.id)
        db.session.add(question1)
        db.session.add(question2)
        db.session.add(question3)
        db.session.commit()

        # Create options
        option1 = Option(text='Option 1', question_id=question1.id)
        option2 = Option(text='Option 2', question_id=question1.id)
        option3 = Option(text='Option 1', question_id=question2.id)
        option4 = Option(text='Option 2', question_id=question2.id)
        option5 = Option(text='Option 1', question_id=question3.id)
        option6 = Option(text='Option 2', question_id=question3.id)
        db.session.add(option1)
        db.session.add(option2)
        db.session.add(option3)
        db.session.add(option4)
        db.session.add(option5)
        db.session.add(option6)
        db.session.commit()

import unittest
from tests.test_base import BaseTestCase
from app.models import UserAnswer
from flask_login import current_user

class TakeSurveyTestCase(BaseTestCase):
    def login_user(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_take_survey_get(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/take-survey/<int:survey_id>' page is requested (GET)
        THEN check that the page is rendered correctly
        """
        with self.client:
            # Login user
            self.login_user('testuser1@example.com', 'password')

            # Get the survey page
            response = self.client.get('/take-survey/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Survey 1', response.data)
            self.assertIn(b'Question 1', response.data)
            self.assertIn(b'Option 1', response.data)

    def test_take_survey_post(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/take-survey/<int:survey_id>' page is submitted (POST)
        THEN check that the survey responses are recorded and user is redirected
        """
        with self.client:
            # Login user
            self.login_user('testuser1@example.com', 'password')

            # Submit the survey
            response = self.client.post('/take-survey/1', data=dict(
                question_1=1,  # Assuming the option ID for 'Option 1' of 'Question 1'
                question_2=3   # Assuming the option ID for 'Option 1' of 'Question 2'
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Survey Dashboard', response.data)

            # Check that the user answers are recorded
            answers = UserAnswer.query.filter_by(user_id=current_user.id).all()
            self.assertEqual(len(answers), 2)
            self.assertEqual(answers[0].option_id, 1)
            self.assertEqual(answers[1].option_id, 3)

if __name__ == '__main__':
    unittest.main()
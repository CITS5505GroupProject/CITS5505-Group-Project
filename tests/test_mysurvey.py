import unittest
from tests.test_base import BaseTestCase
from app.models import Survey

class MySurveyTestCase(BaseTestCase):
    def login_user(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def test_my_survey_page(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/my-survey/<int:user_id>' page is requested (GET)
        THEN check that the response is valid and contains the correct surveys for the user
        """
        # Login user
        self.login_user('testuser1@example.com', 'password')

        with self.client:
            # Access the user's survey page
            response = self.client.get('/my-survey/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Survey 1', response.data)

            
            # Ensure surveys from other users are not included
            self.assertNotIn(b'Survey 2', response.data)

    def test_delete_survey(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/delete-survey/<int:survey_id>' route is accessed (POST)
        THEN check that the survey is deleted from the database
        """
        # Login user
        self.login_user('testuser1@example.com', 'password')

        with self.client:

            # Delete the survey
            response = self.client.delete('/survey/delete/1', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Survey deleted successfully', response.data)

            # Check that the survey has been deleted
            survey = Survey.query.get(1)
            self.assertIsNone(survey)


if __name__ == '__main__':
    unittest.main()
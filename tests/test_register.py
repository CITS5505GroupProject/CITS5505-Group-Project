import unittest
from flask import url_for
from app.models import User
from tests.test_base import BaseTestCase

class RegisterTestCase(BaseTestCase):
    def test_register_page_loads(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/register' page is requested (GET)
        THEN check that the response is valid and the form is displayed
        """
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)
        self.assertIn(b'Username', response.data)
        self.assertIn(b'Email', response.data)
        self.assertIn(b'Password', response.data)
        self.assertIn(b'Confirm Password', response.data)

    def test_successful_registration(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/register' page is posted to (POST) with valid data
        THEN check that the user is registered and redirected to the login page
        """
        response = self.client.post('/register', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        
        # Check that the user is in the database
        user = User.query.filter_by(email='newuser@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')


    def test_registration_with_existing_email(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/register' page is posted to (POST) with an existing email
        THEN check that the user is not registered and an error message is displayed
        """
        self.client.post('/register', data=dict(
            username='uniqueuser',
            email='existingemail@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)

        # Try to register with the same email
        response = self.client.post('/register', data=dict(
            username='anotheruser',
            email='existingemail@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username or email already exists. Please use a different one.', response.data)

if __name__ == '__main__':
    unittest.main()

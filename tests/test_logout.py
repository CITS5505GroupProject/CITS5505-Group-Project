import unittest
from flask_login import current_user
from tests.test_base import BaseTestCase

class LogoutTestCase(BaseTestCase):
    def login_user(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)


    # test the user is logged out
    def test_logout(self):
        with self.client:
        # Login user
            self.login_user('testuser2@example.com', 'password')

            # Check that the user is logged in
            self.assertTrue(current_user.is_authenticated)

            # Access the logout route
            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Shape the Future with Every Survey', response.data) 

            # Check that the user is logged out
            self.assertFalse(current_user.is_authenticated)

    # test user is redirect to index page after logout
    def test_logout_redirect(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/logout' route is accessed (GET)
        THEN check that the user is redirected to the index page
        """
        with self.client:
        # Login user
            self.login_user('testuser2@example.com', 'password')

            # Access the logout route
            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Shape the Future with Every Survey', response.data) 

if __name__ == '__main__':
    unittest.main()

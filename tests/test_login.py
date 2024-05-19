import unittest
from flask_login import current_user
from app.models import User
from tests.test_base import BaseTestCase

class LoginTestCase(BaseTestCase):
    #test whether the login page rendered
    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    #test case when user login successfully
    def test_successful_login(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                email='testuser1@example.com',
                password='password'
            ), follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Profile', response.data)
            
            # Access the current_user proxy
            with self.client.session_transaction() as session:
                user_id = session['_user_id']
                user = User.query.get(int(user_id))
                self.assertIsNotNone(user)
                self.assertTrue(current_user.is_authenticated)
                self.assertEqual(current_user.email, 'testuser1@example.com')

    # test case when invalid user account and password are given
    def test_invalid_login(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                email='invalid@example.com',
                password='password'
            ), follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Username or email is incorrect, try again.', response.data)
            self.assertFalse(current_user.is_authenticated)

    # test links under login page work
    def test_login_links(self):
        with self.client:
            response = self.client.get('/login')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Sign Up', response.data)
            self.assertIn(b'Forget Password?', response.data)

            # Check the 'Sign Up' link
            response = self.client.get('/register')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Register', response.data)

            # Check the 'Forgot Password' link
            response = self.client.get('/reset-password')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Reset Password', response.data)

if __name__ == '__main__':
    unittest.main()

import unittest
import os
from flask_login import current_user, login_user
from app.models import User
from tests.test_base import BaseTestCase

class UpdateProfileTestCase(BaseTestCase):
    def login_user(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    # test update profile page is correctly loaded
    def test_update_profile_page_loads(self):
        # Login user
        self.login_user('testuser1@example.com', 'password')

        # Access the update profile page
        response = self.client.get('/update_profile/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update Profile', response.data)
        self.assertIn(b'Username', response.data)
        self.assertIn(b'Profile Picture', response.data)

    # test whether update profile page update data correctly
    def test_successful_profile_update(self):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/update_profile/<int:user_id>' page is posted to (POST) with valid data
        THEN check that the user's profile is updated and the user is redirected
        """
        # Login user
        self.login_user('testuser1@example.com', 'password')

        # Mock the file upload path
        mock_upload_folder = os.path.join(os.getcwd(), 'tests', 'uploads')
        os.makedirs(mock_upload_folder, exist_ok=True)
        self.app.config['UPLOAD_FOLDER'] = mock_upload_folder

        # Create a dummy file to upload
        dummy_file_path = os.path.join(mock_upload_folder, 'dummy.jpg')
        with open(dummy_file_path, 'wb') as f:
            f.write(os.urandom(24))

        with open(dummy_file_path, 'rb') as dummy_file:
            # Submit the update profile form
            response = self.client.post('/update_profile/1', data=dict(
                username='updateduser',
                profile_pic=dummy_file
            ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Update Profile', response.data)

        # Check that the user's profile is updated in the database
        user = User.query.get(1)
        self.assertEqual(user.username, 'updateduser')
        self.assertTrue(os.path.exists(os.path.join(self.app.config['UPLOAD_FOLDER'], 'dummy.jpg')))

    # check whether user can access to other user's page
    def test_update_profile_unauthorized(self):
        # Login user
        self.login_user('testuser1@example.com', 'password')

        # Try to access another user's update profile page
        response = self.client.get('/update_profile/2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()

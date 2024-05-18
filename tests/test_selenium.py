import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from app import create_app, db
from app.models import User

class RegistrationTest(unittest.TestCase):
    def setUp(self):
        # Set up the Flask application context and test client
        self.app = create_app(config_name='TESTING')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Set up the WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)  # Wait implicitly for elements to be ready before attempting interactions

    def test_register(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/register')  # Navigate to the registration page

        # Find form fields and fill them out
        username_field = driver.find_element(By.NAME, 'username')
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')
        confirm_password_field = driver.find_element(By.NAME, 'confirm_password')

        username_field.send_keys('seleniumuser')
        email_field.send_keys('seleniumuser@example.com')
        password_field.send_keys('password')
        confirm_password_field.send_keys('password')

        # Submit the form
        confirm_password_field.send_keys(Keys.RETURN)

        # Wait for a while to let the page load
        time.sleep(2)

        # Check that the user is redirected to the login page
        self.assertIn('login', driver.current_url)
        self.assertIn('Login', driver.page_source)

    def tearDown(self):
        # Delete the user created during the test
        user = User.query.filter_by(email='seleniumuser@example.com').first()
        if user:
            db.session.delete(user)
            db.session.commit()

        # Close the browser window
        self.driver.quit()

        # Remove the Flask application context and drop the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()

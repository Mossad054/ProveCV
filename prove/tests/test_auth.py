import os
import tempfile
import unittest
from flask import url_for
from werkzeug.security import generate_password_hash
from .app import app, init_db
from .auth import User
import sqlite3

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a temporary database and configure the app for testing
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['DATABASE'] = self.db_path
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.client = app.test_client()
        init_db()

        # Create a test user
        with app.app_context():
            conn = sqlite3.connect(app.config['DATABASE'])
            c = conn.cursor()
            c.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                ('testuser', 'test@example.com', generate_password_hash('password'))
            )
            conn.commit()
            conn.close()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_signup(self):
        # Test user signup
        response = self.client.post('/signup', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        
        self.assertIn(b'Registration successful!', response.data)

    def test_login(self):
        # Test user login
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)
        
        self.assertIn(b'Login successful!', response.data)

    def test_failed_login(self):
        # Test failed login due to incorrect password
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        self.assertIn(b'Please check your login details and try again.', response.data)

    def test_logout(self):
        # Log in first
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password'
        }, follow_redirects=True)

        # Test logout
        response = self.client.get('/logout', follow_redirects=True)
        
        self.assertIn(b'You have been logged out.', response.data)

    def test_signup_existing_user(self):
        # Test signup with an email that already exists
        response = self.client.post('/signup', data={
            'username': 'anotheruser',
            'email': 'test@example.com',  # Existing email
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        
        self.assertIn(b'Email already exists', response.data)

if __name__ == '__main__':
    unittest.main()

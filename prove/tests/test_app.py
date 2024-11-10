import os
import unittest
import tempfile
from flask import url_for
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, init_db
import sqlite3
#App test case
class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database and initialize the app context."""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret'
        self.app = app.test_client()
        with app.app_context():
            init_db()  
    #Tear down
    def tearDown(self):
        """Close and remove the temporary database."""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
#index route
    def test_index_route(self):
        """Test the index route for a successful response."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Automate Resume Tailoring', response.data)
#regsiter route
    def test_register_route(self):
        """Test the registration route for rendering the form."""
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)
#require logins route
    def test_create_resume_route_requires_login(self):
        """Test that the create resume route requires login."""
        response = self.app.get('/create')
        self.assertEqual(response.status_code, 302)  
#create resume route
    def test_create_resume(self):
        """Test creating a resume and saving it in the database."""
        with app.test_client() as client:
            # Log in a user
            with client.session_transaction() as sess:
                sess['user_id'] = 1  

            # Post resume data
            response = client.post('/create', data={
                'name': 'John Doe',
                'email': 'johndoe@example.com',
                'phone': '123456789',
                'summary': 'A passionate software developer.',
                'experience': '3 years at XYZ Company',
                'education': 'Bachelor\'s in Computer Science',
                'skills': 'Python, Flask, SQL'
            })
            self.assertEqual(response.status_code, 302)  
            # Redirects after successful creation

            # Verify resume exists in the database
            conn = sqlite3.connect('resumes.db')
            c = conn.cursor()
            c.execute('SELECT * FROM resumes WHERE name = ?', ('John Doe',))
            resume = c.fetchone()
            conn.close()
            self.assertIsNotNone(resume)
#test view resume route
    def test_view_resume_route(self):
        """Test viewing a resume by ID."""
        # First, create a resume for testing
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        c.execute('''INSERT INTO resumes (name, email, phone, summary, experience, education, skills, user_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                  ('Jane Doe', 'janedoe@example.com', '123456789', 'Experienced developer',
                   '5 years at ABC Corp', 'Master\'s in Computer Science', 'Python, Django', 1))
        resume_id = c.lastrowid
        conn.commit()
        conn.close()

        # Test viewing the resume
        response = self.app.get(f'/view/{resume_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jane Doe', response.data)
#test edit resume route
    def test_edit_resume_route(self):
        """Test editing a resume."""
       
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        c.execute('''INSERT INTO resumes (name, email, phone, summary, experience, education, skills, user_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                  ('Jack Smith', 'jacksmith@example.com', '987654321', 'Software Engineer',
                   '5 years at DEF Ltd', 'Bachelor\'s in Engineering', 'Java, Spring', 1))
        resume_id = c.lastrowid
        conn.commit()
        conn.close()

        # Edit resume
        response = self.app.post(f'/edit/{resume_id}', data={
            'name': 'Jack Smith',
            'email': 'jacksmith_updated@example.com',
            'phone': '987654321',
            'summary': 'Updated software engineer summary.',
            'experience': '6 years at DEF Ltd',
            'education': 'Bachelor\'s in Engineering',
            'skills': 'Java, Spring, Docker'
        })
        self.assertEqual(response.status_code, 302)

        # Verify the resume was updated
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        c.execute('SELECT email FROM resumes WHERE id = ?', (resume_id,))
        updated_email = c.fetchone()[0]
        conn.close()
        self.assertEqual(updated_email, 'jacksmith_updated@example.com')
#display user routes
    def test_my_resumes_route(self):
        """Test displaying the current user's resumes."""
        with app.test_client() as client:
            # Log in a user
            with client.session_transaction() as sess:
                sess['user_id'] = 1 

            response = client.get('/my-resumes')
            self.assertEqual(response.status_code, 200)
#test ehnancement
    def test_enhance_text_route(self):
        """Test the AI text enhancement route with sample text."""
        response = self.app.post('/enhance-text', json={'text': 'Software developer'})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('enhanced_text', json_data)
#End of test case
if __name__ == '__main__':
    unittest.main()

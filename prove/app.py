from flask import Flask, render_template, request, redirect, url_for, send_file, flash, make_response, jsonify
import sqlite3
from datetime import datetime
import os
from flask_login import LoginManager, login_required, current_user
from auth import auth_bp, User 
import pdfkit
from routes.ai_routes import ai_bp
import google.generativeai as genai
from routes.ai_routes import ai_bp
from dotenv import load_dotenv
import os

load_dotenv()  # Add this line if it's not already present
app = Flask(__name__)

# Add this right after creating the Flask app
app.secret_key = os.environ.get('mossad') or os.urandom(24)

# Configure Gemini API
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment variables")
    
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Redirect to the login view if not logged in
# Register the AI blueprint
app.register_blueprint(ai_bp, url_prefix='/ai')

# Load the user from the database
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(id=user[0], username=user[1], email=user[2], password_hash=user[3])  # Update as per your User model structure
    return None

# Database initialization
def init_db():
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    
    # First, create a new resumes table with user_id if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        summary TEXT,
        experience TEXT,
        education TEXT,
        skills TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Add users table for authentication
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )''')
    
    # Check if user_id column exists, if not add it
    try:
        c.execute('SELECT user_id FROM resumes LIMIT 1')
    except sqlite3.OperationalError:
        # Column doesn't exist, so add it
        c.execute('ALTER TABLE resumes ADD COLUMN user_id INTEGER')
        
    conn.commit()
    conn.close()

# Initialize database when app starts
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
@login_required  # Require login to create a resume
def create():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        summary = request.form['summary']
        experience = request.form['experience']
        education = request.form['education']
        skills = request.form['skills']
        
        # Save to database with user_id
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        c.execute('''INSERT INTO resumes 
                     (name, email, phone, summary, experience, education, skills, user_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (name, email, phone, summary, experience, education, skills, current_user.id))
        resume_id = c.lastrowid
        conn.commit()
        conn.close()
        
        flash('Resume created successfully!', 'success')
        return redirect(url_for('view_resume', id=resume_id))
    
    return render_template('create.html')

@app.route('/view/<int:id>')
@login_required  # Require login to view a resume
def view_resume(id):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM resumes WHERE id = ?', (id,))
    resume = c.fetchone()
    conn.close()
    
    if resume:
        return render_template('view.html', resume=resume)
    return 'Resume not found', 404

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required  # Require login to edit a resume
def edit_resume(id):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        # Update resume
        c.execute('''UPDATE resumes 
                     SET name=?, email=?, phone=?, summary=?, experience=?, education=?, skills=?
                     WHERE id=?''', (
            request.form['name'],
            request.form['email'],
            request.form['phone'],
            request.form['summary'],
            request.form['experience'],
            request.form['education'],
            request.form['skills'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('view_resume', id=id))
    
    # Get existing resume data
    c.execute('SELECT * FROM resumes WHERE id = ?', (id,))
    resume = c.fetchone()
    conn.close()
    
    if resume:
        return render_template('edit.html', resume=resume)
    return 'Resume not found', 404

@app.route('/my-resumes')
@login_required
def my_resumes():
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM resumes WHERE user_id = ? ORDER BY created_at DESC', (current_user.id,))
    resumes = c.fetchall()
    conn.close()
    
    return render_template('my_resumes.html', resumes=resumes)

# Add new route for AI enhancement
@app.route('/enhance-text', methods=['POST'])
def enhance_text():
    data = request.get_json()
    text = data.get('text', '')
    try:
        # Return unmodified text if enhancement fails
        return jsonify({'enhanced_text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<int:id>')
@login_required
def download_resume(id):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM resumes WHERE id = ?', (id,))
    resume = c.fetchone()
    conn.close()
    
    if resume:
        # Generate HTML content
        html_content = render_template('export.html', resume=resume)
        
        # Configure pdfkit options
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8"
        }
        
        # Generate PDF from HTML
        pdf = pdfkit.from_string(html_content, False, options=options)
        
        # Create response
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=resume_{resume[1]}.pdf'
        
        return response
    return 'Resume not found', 404
from flask import render_template, flash, redirect, url_for
from forms import RegistrationForm

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Here you would typically:
        # 1. Hash the password
        # 2. Create a new user in your database
        # 3. Log them in
        # 4. Redirect to dashboard
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Register the authentication blueprint
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    os.makedirs('static/exports', exist_ok=True)
    app.run(debug=True)

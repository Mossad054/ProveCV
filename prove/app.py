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
from werkzeug.utils import secure_filename
import PyPDF2
import docx
from flask import render_template, flash, redirect, url_for
from forms import RegistrationForm

load_dotenv()
app = Flask(__name__)

app.secret_key = os.environ.get('mossad') or os.urandom(24)

# Configuring  Gemini API
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment variables")
    
genai.configure(api_key=GOOGLE_API_KEY)
# Initializing the model
model = genai.GenerativeModel('gemini-pro')

# Initializing Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 
# Registering the AI blueprint
app.register_blueprint(ai_bp, url_prefix='/ai')
# Registers the authentication blueprint
app.register_blueprint(auth_bp)


# Loading the user from the database
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(id=user[0], username=user[1], email=user[2], password_hash=user[3]) 
    return None

# Database initialization
def init_db():
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    
    # First, creates a new resumes table with user_id if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        summary TEXT,
        experience TEXT,
        education TEXT,
        skills TEXT,
        referees TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Addingusers table for authentication
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )''')
    
    # Checksif user_id column exists, if not adds it
    try:
        c.execute('SELECT user_id FROM resumes LIMIT 1')
    except sqlite3.OperationalError:
        # IF column doesn't exist, so add it
        c.execute('ALTER TABLE resumes ADD COLUMN user_id INTEGER')
        
    conn.commit()
    conn.close()

# Initialize database when app starts
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
# Requires login to create a resume
@login_required  
def create():
    if request.method == 'POST':
        # Gets form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        summary = request.form['summary']
        experience = request.form['experience']
        education = request.form['education']
        skills = request.form['skills']
        referees = request.form.get('referees', '')         
        # Formats referees data if is not empty.
        if referees:
            referees = referees.strip() 
        # Saves to database with user_id
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        # Inserts data into the database
        c.execute('''INSERT INTO resumes 
                     (name, email, phone, summary, experience, education, skills, referees, user_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (name, email, phone, summary, experience, education, skills, referees, current_user.id))
        resume_id = c.lastrowid
        conn.commit()
        conn.close()
        #updates whethers resume has been created successfully
        flash('Resume created successfully!', 'success')
        return redirect(url_for('view_resume', id=resume_id))
    # Renders the create template
    return render_template('create.html')

# Function to view a resume
@app.route('/view/<int:id>')
# Require login to view a resume
@login_required  
def view_resume(id):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM resumes WHERE id = ?', (id,))
    resume = c.fetchone()
    conn.close()
    # If resume is found, renders the view template.
    if resume:
        return render_template('view.html', resume=resume)
    # If resume is not found, returns a 404 error.
    return 'Resume not found', 404

# Function to edit a resume
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
# Requires login to edit a resume
@login_required  
def edit_resume(id):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    # If the method is POST, updates the resume.
    if request.method == 'POST':
        # Updates the resume
        c.execute('''UPDATE resumes 
                     SET name=?, email=?, phone=?, summary=?, experience=?, education=?, skills=?, referees=?
                     WHERE id=?''', (
            request.form.get('name', ''),
            request.form.get('email', ''),
            request.form.get('phone', ''),
            request.form.get('summary', ''),
            request.form.get('experience', ''),
            request.form.get('education', ''),
            request.form.get('skills', ''),
            request.form.get('referees', ''),
            id
        ))
        conn.commit()
        conn.close()
        # Redirects to the view resume page.
        return redirect(url_for('view_resume', id=id))
    
    # Gets existing resume data
    c.execute('SELECT * FROM resumes WHERE id = ?', (id,))
    resume = c.fetchone()
    conn.close()
    # If resume is found, renders the edit template.
    if resume:
        return render_template('edit.html', resume=resume)
    return 'Resume not found', 404

# Function to view all resumes
@app.route('/my-resumes')
# Requires login to view all resumes.
@login_required
def my_resumes():
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    # Selects all resumes from the database for the current user, ordered by creation date.
    c.execute('SELECT * FROM resumes WHERE user_id = ? ORDER BY created_at DESC', (current_user.id,))
    resumes = c.fetchall()
    conn.close()
    # Renders the my_resumes template.
    return render_template('my_resumes.html', resumes=resumes)

# Add new route for AI enhancement
@app.route('/enhance-text', methods=['POST'])
# Function to enhance text.
def enhance_text():
    data = request.get_json()
    text = data.get('text', '')
    try:
        model = genai.GenerativeModel('gemini-pro')
        # Prompts the model to enhance the text while maintaining its core meaning.
        prompt = f"Please enhance this professional text while maintaining its core meaning: {text}"
        response = model.generate_content(prompt)
        return jsonify({'enhanced_text': response.text})
    except Exception as e:
        # Returns to original text if enhancement fails.
        return jsonify({'enhanced_text': text, 'error': str(e)})
    
# Function to download a resume.
@app.route('/download/<int:id>')
# Requires login to download a resume.
@login_required
def download_resume(id):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM resumes WHERE id = ?', (id,))
    resume = c.fetchone()
    conn.close()
    # If resume is found, generates HTML content.
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

# Function to register a user.
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Updates the database with the new user.
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    # Renders the register template.
    return render_template('register.html', form=form)

# Function to display the FAQ.
@app.route('/faq')
def faq():
    # Displays the FAQ.
    faqs = [
        {
            "question": "What is ProveCV?",
            "answer": "ProveCV is an AI-powered resume-building platform that helps users create and enhance resumes to be professional, customized, and ATS-compliant."
        },
        {
            "question": "How does ProveCV work?",
            "answer": "ProveCV allows you to input your resume details or upload an existing document. It uses AI to refine your content, suggest improvements, and help you choose from multiple templates that best fit your field and goals."
        },
        {
            "question": "Can I use ProveCV to tailor my resume to specific job applications?",
            "answer": "Yes! You can add job descriptions or key responsibilities from advertised roles, and ProveCV's AI will help align your experience to those roles, enhancing relevance for potential employers."
        },
        {
            "question": "What resume formats are available?",
            "answer": "ProveCV provides various ATS-compliant templates and formats that are customizable. You can also download your finished resume as a PDF file."
        },
        {
            "question": "Is my information stored securely on ProveCV?",
            "answer": "Yes, we prioritize data security. Your data is securely stored, and access is restricted. We also provide you with the option to delete your resumes or account at any time."
        },
        {
            "question": "Do I need an account to use ProveCV?",
            "answer": "Yes, creating an account allows ProveCV to save your resumes and previous work for easy access and future edits. However, you can preview some features without an account."
        },
        {
            "question": "Does ProveCV support resume editing for existing resumes?",
            "answer": "Absolutely! You can upload your existing resume, and ProveCV will assist in enhancing and formatting it according to your specifications and preferred template."
        }
    ]
    # Renders the FAQ template.
    return render_template('faq.html', faqs=faqs)

# Defines the upload folder path relative to the app directory.
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# Creates the uploads directory if it doesn't exist.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
# Configures the upload folder path.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file is allowed.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from a PDF file.
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to extract text from a DOCX file.
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text
#
@app.route('/upload_resume', methods=['POST'])
@login_required
def upload_resume():
    try:
        if 'resume' not in request.files:
            flash('No file part in the request', 'error')
            return redirect(url_for('create'))
        
        file = request.files['resume']
        # Checks if the file is selected.
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('create'))
        # Checks if the file is allowed.
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload PDF, DOC, or DOCX files only.', 'error')
            return redirect(url_for('create'))
    
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Save and process file
                file.save(file_path)
                
                try:
                    if filename.endswith('.pdf'):
                        text = extract_text_from_pdf(file_path)
                    else:
                        text = extract_text_from_docx(file_path)
                    # updates files upload successfully.
                    session['uploaded_resume_text'] = text
                    flash('Resume uploaded and processed successfully!', 'success')
                    
                    #if file is in the correct format, returns to the create page.
                except Exception as e:
                    app.logger.error(f"File processing error: {str(e)}")
                    flash('Error processing file content. Please try a different file.', 'error')
                
                finally:
                    # Cleans up the uploaded file.
                    if os.path.exists(file_path):
                        os.remove(file_path)
                
                return redirect(url_for('create'))
                
            except Exception as e:
                app.logger.error(f"File save error: {str(e)}")
                flash('Error saving file. Please try again.', 'error')
                return redirect(url_for('create'))
    # If file is not uploaded successfully returns an error.
    except Exception as e:
        app.logger.error(f"Upload error: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('create'))
    
# Function to save the referee data.
@app.route('/save-referee', methods=['POST'])
def save_referee():
    referee_data = request.form.get('referees')
    # Processes and saves the referee data.
    return jsonify({
        'success': True,
        'referee_text': referee_data  
        # Returns the formatted text.
    })
# Runs the app.
if __name__ == '__main__':
    os.makedirs('static/exports', exist_ok=True)
    app.run(debug=True)

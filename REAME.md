ProveCV - AI-Powered Resume Builder
ProveCV is an AI-driven platform designed to help users quickly create customized, ATS-compliant resumes. With easy-to-use templates, AI-assisted content generation, and secure data storage, ProveCV simplifies the resume creation process, helping users build professional, job-ready resumes.

Table of Contents
Features
Technology Stack
How It Works
Architecture and Data Flow
Setup and Installation
Windows Installation
Linux Installation
Usage
Features
Effortless Resume Creation: User-friendly templates and AI-powered suggestions help users build polished resumes with ease.
AI-Assisted Content: Automatic content enhancement, job-specific keyword suggestions, and customizable descriptions to improve resume relevance.
Secure Data Storage: User data and resumes are securely stored and encrypted for privacy.
Downloadable Formats: Resumes can be downloaded in PDF or DOC formats.
Job Tailoring: Allows users to input specific job descriptions, enabling AI to tailor content to specific roles.
Resume Templates: A selection of professionally designed, ATS-compliant templates that are easy to customize.
Technology Stack
Frontend: HTML, CSS, JavaScript (for interactive UI and templating)
Backend: Python Flask (handling server requests and AI integration)
Database: SQLite (for lightweight, on-device data storage)
AI Model: OpenAI API (to power AI-driven content suggestions and improvements)
PDF Generation: WeasyPrint (for generating downloadable resume files)
How It Works
User Registration: Users create an account, which allows them to access their saved resumes and data.
Resume Template Selection: Users choose from a range of professional, ATS-compliant templates.
Data Input: Users fill in their details (personal info, experiences, education, skills, etc.), and ProveCV provides AI-powered content suggestions.
Resume Customization: Users can tweak the look and feel of their resume, as well as tailor specific sections.
Download or Save: Users can download their resume in PDF or DOC format or save it on ProveCV for future editing.
Architecture and Data Flow
The architecture follows a Model-View-Controller (MVC) pattern for maintainability, with Flask serving as the backend framework. The data flow is as follows:

User Request: Users interact with the frontend (HTML/CSS/JavaScript), which sends requests to the Flask server.
Server Processing: Flask processes these requests, handles AI-enhanced content generation with OpenAI API, and manages user data.
Database Storage: User data, resumes, and settings are stored in SQLite, allowing users to access previously created resumes.
PDF Generation and Download: Upon request, the resume is formatted and generated as a PDF using WeasyPrint.
Diagram
plaintext
Copy code
                   +-------------------+
                   |    Frontend       |
                   |  (HTML, CSS, JS)  |
                   +---------+---------+
                             |
                             |
                             v
                   +-------------------+
                   |    Flask API      |
                   | (Controller)      |
                   +---------+---------+
                             |
               +-------------+--------------+
               |                            |
               v                            v
     +-------------------+           +---------------+
     |     OpenAI API    |           |    SQLite     |
     |  (AI Content Gen) |           |  (Data Store) |
     +-------------------+           +---------------+
                             |
                             v
                     +---------------+
                     |    WeasyPrint  |
                     | (PDF Gen)      |
                     +---------------+
Setup and Installation
Prerequisites
Python 3.x
Pip package manager
OpenAI API key (for AI content generation)
WeasyPrint (for PDF generation)
Windows Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/mossad054/prove.git
cd prove
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Up Environment Variables: Create a .env file in the root directory and add your OpenAI API key:

plaintext
Copy code
OPENAI_API_KEY=your_openai_api_key_here
Run Database Migrations:

bash
Copy code
python migrate.py
Start the Application:

bash
Copy code
python app.py
Visit http://127.0.0.1:5000 in your browser to access ProveCV.

Linux Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/mossad054/prove.git
cd prove
Install Dependencies:

bash
Copy code
pip3 install -r requirements.txt
Set Up Environment Variables: Create a .env file in the root directory and add your OpenAI API key:

plaintext
Copy code
OPENAI_API_KEY=your_openai_api_key_here
Run Database Migrations:

bash
Copy code
python3 migrate.py
Start the Application:

bash
Copy code
python3 app.py
Visit http://127.0.0.1:5000 in your browser to access ProveCV.

Usage
Sign Up: Register a new account or log in to access the resume builder.
Select a Template: Choose from a variety of professional templates.
Input Details: Fill in personal information, work experience, education, and skills. ProveCV’s AI will assist in enhancing your content.
Customize and Download: Customize your resume’s layout and style, then download it as a PDF or DOC.
Contributing
We welcome contributions! If you’re interested in contributing to ProveCV, please fork the repository, make your changes, and submit a pull request.
## ProveCV - AI-Powered Resume Builder
ProveCV is an AI-driven platform designed to help users create customized, ATS-compliant resumes. 
With easy-to-use templates, AI-assisted content generation, and secure data storage.
ProveCV simplifies the resume creation process, helping users build professional, job-ready resumes.

 ## Table of Contents
- Features
- Technology Stack
- How It Works
- Architecture and Data Flow](#architecture-and-data-flow)
- Setup and Installation.
  - Windows Installation
  - Linux Installation
- Usage
- Contributing

## Features
- **Effortless Resume Creation**: User-friendly templates and AI-powered suggestions help users build polished resumes with ease.
- **AI-Assisted Content**: Automatic content enhancement, job-specific keyword suggestions, and customizable descriptions to improve resume relevance.
- **Downloadable Formats**: Resumes can be downloaded in PDF formats.
- **Job Tailoring**: Allows users to input specific job descriptions, enabling AI to tailor content to specific roles.
- **Resume Templates**: A selection of professionally designed, ATS-compliant templates that are easy to customize.

## Technology Stack.
- **Frontend**: HTML, CSS, JavaScript (for interactive UI and templating)
- **Backend**: Python Flask (handling server requests and AI integration)
- **Database**: SQLite.
- **AI Model**: Google's Gemini Pro API (to power AI-driven content suggestions and improvements)
- **PDF Generation**: WeasyPrint (for generating downloadable resume files).

## How It Works
1. **User Registration**: Users create an account, which allows them to access their saved resumes and data.
2. **Resume Template Selection**: Users choose from a range of professional, ATS-compliant templates.
3. **Data Input**: Users fill in their details (personal info, experiences, education, skills, etc.), and ProveCV provides AI-powered content suggestions.
4. **Resume Customization**: Users can customize  the look and feel of their resume, as well as tailor specific sections.
5. **Download or Save**: Users can download their resume in PDF or save it on ProveCV for future editing.

## Architecture and Data Flow
The architecture follows a Model-View-Controller (MVC) pattern for maintainability, with Flask serving as the backend framework. The data flow is as follows:

1. **User Request**: Users interact with the frontend (HTML/CSS/JavaScript), which sends requests to the Flask server.
2. **Server Processing**: Flask processes these requests, handles AI-enhanced content generation with Gemini Pro API, and manages user data.
3. **Database Storage**: User data, resumes, and settings are stored in SQLite, allowing users to access previously created resumes.
4. **PDF Generation and Download**: Upon request, the resume is formatted and generated as a PDF using WeasyPrint.

## Setup and Installation.

  # Clone the Repository

git clone https://github.com/yourusername/provecv.git
cd Provecv
  #  Install Dependencies
pip install -r requirements.txt
  # Set Up Environment Variables
Create a .env file in the root directory and add:
GOOGLE_API_KEY=your_google_api_key_here (input your google_api_key)
  # Run Database Migrations
python migrate.py
# Start the Application
  # on Linux/Bash
python app.py
  # on Windows 
  ## Prerequisites
   1. **Python Installation**
   - Download Python 3.x from [python.org](https://www.python.org/downloads/)
  2. 
   # Activate virtual environment
   .\venv\Scripts\activate
### Prerequisites
- Python 3.x
- Pip package manager
- Google Cloud API key (for AI content generation)
- WeasyPrint (for PDF generation)
Visit http://127.0.0.1:5000 in your browser to access ProveCV.
### Windows Installation
Visit http://127.0.0.1:5000 in your browser to access ProveCV.
### Usage 

Visit http://127.0.0.1:5000 in your browser to access ProveCV.

## Usage
1. **Sign Up**: Register a new account or log in to access the resume builder.
2. **Select a Template**: Choose from a variety of professional templates.
3. **Input Details**: Fill in personal information, work experience, education, and skills. ProveCV's AI will assist in enhancing your content.
4. **Customize and Download**: Customize your resume's layout and style, then download it as a PDF.

## Contributing
We welcome contributions! If you're interested in contributing to ProveCV:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request.

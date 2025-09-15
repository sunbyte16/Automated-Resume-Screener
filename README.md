<div align="center">

# Automated Resume Screener

AI-powered resume analysis and job-match scoring for job seekers and recruiters.

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![spaCy](https://img.shields.io/badge/spaCy-NLP-09A3D5?logo=spacy&logoColor=white)](https://spacy.io/)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](../../pulls)


<br/>

<a href="https://github.com/sunbyte16">![GitHub](https://img.shields.io/badge/GitHub-sunbyte16-181717?logo=github)</a>
<a href="https://www.linkedin.com/in/sunil-kumar-bb88bb31a/">![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil%20Sharma-0A66C2?logo=linkedin&logoColor=white)</a>
<a href="https://lively-dodol-cc397c.netlify.app">![Portfolio](https://img.shields.io/badge/Portfolio-Visit-1ABC9C?logo=vercel&logoColor=white)</a>

<br/>

<img alt="Tech icons" src="https://skillicons.dev/icons?i=python,flask,sklearn,bootstrap,sqlite,git&perline=6" />

</div>

---

A powerful Flask-based web application that uses AI and machine learning to automatically analyze resumes and match them against job descriptions. The system extracts key information from resumes, calculates similarity scores, and provides detailed insights to help both job seekers and recruiters.

## 📚 Table of Contents

- [🚀 Features](#-features)
- [🛠️ Installation](#️-installation)
- [📁 Project Structure](#-project-structure)
- [🎯 Usage](#-usage)
- [🔧 Configuration](#-configuration)
- [🧠 How It Works](#-how-it-works)
- [🚀 Deployment](#-deployment)
- [🧪 Testing](#-testing)
- [📊 API Endpoints](#-api-endpoints)
- [🔒 Security Considerations](#-security-considerations)
- [🐛 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)
- [📞 Support](#-support)

## 🚀 Features

### For Job Seekers
- **Resume Upload**: Support for PDF and DOCX files
- **AI-Powered Analysis**: Automatic extraction of skills, experience, and education
- **Match Scoring**: Get a percentage score showing how well your resume matches job requirements
- **Detailed Insights**: View matched and missing keywords
- **Improvement Tips**: Receive personalized suggestions to enhance your resume
- **Job Browsing**: Browse available job postings and apply directly

### For Recruiters/Admins
- **Admin Dashboard**: Comprehensive overview of all resumes and job postings
- **Resume Management**: View, download, and manage all submitted resumes
- **Job Posting Management**: Create, edit, and manage job descriptions
- **User Management**: Manage user accounts and admin privileges
- **Export Functionality**: Export resume data to Excel for further analysis
- **Analytics**: View statistics and trends

### Technical Features
- **Modern UI**: Responsive design with Bootstrap 5
- **Secure Authentication**: User registration, login, and session management
- **File Processing**: Automatic text extraction from PDF and DOCX files
- **NLP Processing**: Uses spaCy for natural language processing
- **Machine Learning**: TF-IDF vectorization and cosine similarity for matching
- **Database**: SQLite database with SQLAlchemy ORM
- **API Endpoints**: RESTful API for resume management

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/sunbyte16/Automated-Resume-Screener.git
cd Automated-Resume-Screener
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

### Step 5: Set Up Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### Step 6: Run the Application
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
Automated-Resume-Screener/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes.py            # Main application routes
│   ├── auth.py              # Authentication routes
│   ├── admin.py             # Admin panel routes
│   ├── forms.py             # WTForms definitions
│   ├── utils.py             # Utility functions for resume processing
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom CSS styles
│   │   └── js/
│   │       └── main.js      # JavaScript functionality
│   └── templates/
│       ├── base.html        # Base template
│       ├── index.html       # Home page
│       ├── jobs.html        # Job listings
│       ├── job_detail.html  # Job details
│       ├── view_resume.html # Resume analysis view
│       ├── profile.html     # User profile
│       ├── auth/
│       │   ├── login.html   # Login page
│       │   ├── register.html # Registration page
│       │   └── create_admin.html # Admin creation
│       └── admin/
│           ├── dashboard.html # Admin dashboard
│           ├── manage_jobs.html # Job management
│           ├── manage_resumes.html # Resume management
│           ├── users.html   # User management
│           └── job_form.html # Job creation/edit form
├── requirements.txt         # Python dependencies
├── run.py                  # Application entry point
└── README.md              # This file
```

## 🎯 Usage

### Getting Started

1. **Register an Account**: Create a new user account or log in
2. **Upload Resume**: Upload your resume in PDF or DOCX format
3. **Browse Jobs**: Look through available job postings
4. **Get Analysis**: View detailed analysis of your resume against job requirements
5. **Improve Resume**: Use the provided tips to enhance your resume

### For Administrators

1. **Access Admin Panel**: Log in with an admin account
2. **Manage Jobs**: Create and edit job postings
3. **View Resumes**: Access all submitted resumes
4. **User Management**: Manage user accounts and permissions
5. **Export Data**: Export resume data for external analysis

## 🔧 Configuration

### Database
The application uses SQLite by default. To use a different database, modify the `SQLALCHEMY_DATABASE_URI` in `app/__init__.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
```

### File Upload
- Maximum file size: 16MB
- Supported formats: PDF, DOCX
- Upload directory: `app/static/uploads/`

### Security
- Change the `SECRET_KEY` in your `.env` file
- Use environment variables for sensitive configuration
- Enable HTTPS in production

## 🧠 How It Works

### Resume Processing Pipeline

1. **File Upload**: User uploads resume file
2. **Text Extraction**: 
   - PDF: Uses PyPDF2 to extract text
   - DOCX: Uses python-docx to extract text
3. **Information Extraction**:
   - Contact information (email, phone)
   - Skills using NLP and keyword matching
   - Work experience with date parsing
   - Education details
4. **Job Matching**:
   - TF-IDF vectorization of resume and job description
   - Cosine similarity calculation
   - Keyword matching analysis
5. **Scoring**: Generate match percentage and insights

### AI/ML Components

- **spaCy**: Natural language processing for text analysis
- **scikit-learn**: TF-IDF vectorization and similarity calculation
- **Custom Algorithms**: Skill extraction and experience parsing
- **Regex Patterns**: Contact information and date extraction

## 🚀 Deployment

### Production Deployment

1. **Set Environment Variables**:
```env
SECRET_KEY=your-production-secret-key
FLASK_ENV=production
DATABASE_URL=your-production-database-url
```

2. **Use a Production WSGI Server**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

3. **Set Up Reverse Proxy** (nginx example):
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

### Manual Testing
1. Test file upload with different formats
2. Verify resume processing accuracy
3. Test user authentication and authorization
4. Check admin panel functionality
5. Validate job matching algorithms

## 📊 API Endpoints

### Public Endpoints
- `GET /` - Home page
- `GET /jobs` - List all jobs
- `GET /job/<id>` - View job details

### Authentication Required
- `POST /upload` - Upload resume
- `GET /resume/<id>` - View resume analysis
- `GET /profile` - User profile
- `GET /api/resumes` - Get user's resumes

### Admin Only
- `GET /admin/` - Admin dashboard
- `GET /admin/resumes` - Manage resumes
- `GET /admin/jobs` - Manage jobs
- `GET /admin/users` - Manage users

## 🔒 Security Considerations

- **File Upload Security**: Validate file types and sizes
- **SQL Injection**: Use SQLAlchemy ORM for safe queries
- **XSS Protection**: Escape user input in templates
- **CSRF Protection**: Use Flask-WTF for form protection
- **Authentication**: Secure session management
- **File Storage**: Store uploaded files outside web root

## 🐛 Troubleshooting

### Common Issues

1. **spaCy Model Not Found**:
```bash
python -m spacy download en_core_web_sm
```

2. **File Upload Errors**:
   - Check file size (max 16MB)
   - Ensure file is PDF or DOCX
   - Verify upload directory permissions

3. **Database Errors**:
   - Check database file permissions
   - Ensure SQLAlchemy is properly configured
   - Run database migrations if needed

4. **Import Errors**:
   - Activate virtual environment
   - Install all requirements
   - Check Python version compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask framework for the web framework
- spaCy for natural language processing
- scikit-learn for machine learning algorithms
- Bootstrap for the UI framework
- All the open-source libraries used in this project

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

---

**Note**: This is a demonstration project. For production use, consider additional security measures, performance optimizations, and comprehensive testing.


---

<div align="center"><strong>Created By <a href="https://github.com/sunbyte16">Sunil Sharma❤️</a></strong></div>
<br/>
<p align="center">
  <a href="https://www.linkedin.com/in/sunil-kumar-bb88bb31a/">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin&logoColor=white" alt="LinkedIn: Connect" />
  </a>
  <a href="https://lively-dodol-cc397c.netlify.app" style="margin-left:8px;">
    <img src="https://img.shields.io/badge/Portfolio-Visit-1ABC9C?logo=firefox&logoColor=white" alt="Portfolio: Visit" />
  </a>
  
</p>

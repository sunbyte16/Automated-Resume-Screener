import os
import re
import json
import PyPDF2
from docx import Document
from flask import current_app
from .models import db, Resume, Job
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Load English language model for spaCy
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    # If the model is not found, download it
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}

def extract_text_from_pdf(file_path):
    """Extract text content from a PDF file."""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
    except Exception as e:
        current_app.logger.error(f"Error extracting text from PDF: {str(e)}")
    return text

def extract_text_from_docx(file_path):
    """Extract text content from a DOCX file."""
    try:
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        current_app.logger.error(f"Error extracting text from DOCX: {str(e)}")
        return ""

def extract_skills(text):
    """Extract skills from text using NLP."""
    # List of common skills (can be expanded)
    common_skills = [
        'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go',
        'django', 'flask', 'react', 'angular', 'vue', 'node.js', 'express', 'spring', 'laravel',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server',
        'aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd',
        'machine learning', 'deep learning', 'data analysis', 'data visualization', 'nlp',
        'agile', 'scrum', 'devops', 'rest api', 'graphql', 'microservices', 'tensorflow', 'pytorch'
    ]
    
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Find skills in the text
    found_skills = [skill for skill in common_skills if skill in text_lower]
    
    # Use spaCy to find noun phrases that might be skills
    doc = nlp(text)
    noun_phrases = set(chunk.text.lower() for chunk in doc.noun_chunks)
    
    # Add any noun phrases that are not too long and not already in found_skills
    for phrase in noun_phrases:
        if 2 <= len(phrase.split()) <= 3 and phrase not in found_skills and len(phrase) < 30:
            found_skills.append(phrase)
    
    return list(set(found_skills))  # Remove duplicates

def extract_experience(text):
    """Extract work experience information."""
    # This is a simplified version - consider using a more sophisticated approach
    experience = {}
    
    # Look for dates that might indicate work periods
    date_pattern = r'(\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4})\s*-\s*((?:(?:Present|Current)|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4})?)'
    
    # Look for job titles (this is very basic and may need refinement)
    title_pattern = r'(?:\n|^)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:\n|$)'
    
    # Find all matches
    date_matches = re.finditer(date_pattern, text, re.IGNORECASE)
    title_matches = re.finditer(title_pattern, text)
    
    # Extract dates and titles (this is a simplified approach)
    dates = [match.group(0).strip() for match in date_matches]
    titles = [match.group(1).strip() for match in title_matches if len(match.group(1).split()) <= 4]  # Limit title length
    
    # Create a simple experience dictionary
    if dates:
        experience['start_date'] = dates[0].split('-')[0].strip()
        experience['end_date'] = dates[0].split('-')[1].strip() if len(dates) > 0 and '-' in dates[0] else 'Present'
    
    if titles:
        experience['most_recent_title'] = titles[0]
    
    return experience

def extract_education(text):
    """Extract education information."""
    education = {}
    
    # Look for degree patterns
    degree_patterns = [
        r'\b(?:B\.?S\.?|Bachelor(?:\'?s)?(?:\s+of\s+Science)?(?:\s+in\s+\w+)?)\b',
        r'\b(?:M\.?S\.?|Master(?:\'?s)?(?:\s+of\s+Science)?(?:\s+in\s+\w+)?)\b',
        r'\b(?:Ph\.?D\.?|Doctor(?:ate)?(?:\s+of\s+Philosophy)?(?:\s+in\s+\w+)?)\b',
        r'\b(?:B\.?A\.?|Bachelor(?:\'?s)?(?:\s+of\s+Arts)?(?:\s+in\s+\w+)?)\b',
        r'\b(?:M\.?A\.?|Master(?:\'?s)?(?:\s+of\s+Arts)?(?:\s+in\s+\w+)?)\b',
        r'\b(?:B\.?E\.?|Bachelor(?:\'?s)?(?:\s+of\s+Engineering)?(?:\s+in\s+\w+)?)\b',
        r'\b(?:M\.?E\.?|Master(?:\'?s)?(?:\s+of\s+Engineering)?(?:\s+in\s+\w+)?)\b',
    ]
    
    # Look for university/school names (simplified)
    school_pattern = r'\b(?:University|College|Institute|School|Academy)\b.*?\n'
    
    # Find all matches
    degrees = []
    for pattern in degree_patterns:
        degrees.extend([match.group(0) for match in re.finditer(pattern, text, re.IGNORECASE)])
    
    schools = [match.group(0).strip() for match in re.finditer(school_pattern, text, re.IGNORECASE)]
    
    # Create education dictionary
    if degrees:
        education['degrees'] = list(set(degrees))  # Remove duplicates
    
    if schools:
        education['schools'] = list(set(schools))  # Remove duplicates
    
    return education

def extract_contact_info(text):
    """Extract contact information from text."""
    contact = {}
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        contact['email'] = emails[0]  # Take the first email found
    
    # Phone number pattern (simplified)
    phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    if phones:
        contact['phone'] = phones[0].strip()
    
    return contact

def calculate_similarity(resume_text, job_description):
    """Calculate similarity score between resume and job description using TF-IDF."""
    if not resume_text or not job_description:
        return 0.0
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        # Fit and transform the texts
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        # Convert to percentage (0-100)
        return round(float(similarity[0][0]) * 100, 2)
    except Exception as e:
        current_app.logger.error(f"Error calculating similarity: {str(e)}")
        return 0.0

def process_resume(resume_id):
    """Process a resume asynchronously to extract information and calculate scores."""
    with current_app.app_context():
        try:
            resume = Resume.query.get(resume_id)
            if not resume:
                return
            
            # Update status to processing
            resume.status = 'processing'
            db.session.commit()
            
            # Extract text based on file type
            file_ext = os.path.splitext(resume.file_path)[1].lower()
            
            if file_ext == '.pdf':
                text = extract_text_from_pdf(resume.file_path)
            elif file_ext == '.docx':
                text = extract_text_from_docx(resume.file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            # Extract information
            contact = extract_contact_info(text)
            skills = extract_skills(text)
            experience = extract_experience(text)
            education = extract_education(text)
            
            # Update resume with extracted information
            if 'email' in contact:
                resume.email = contact['email']
            if 'phone' in contact:
                resume.phone = contact['phone']
            
            # If name not provided, try to extract from filename
            if not resume.name:
                # Simple heuristic: take the first part of the filename as name
                name_parts = os.path.splitext(resume.original_filename)[0].split('_')
                if name_parts:
                    resume.name = ' '.join(part.capitalize() for part in name_parts[0].split())
            
            # Store extracted data as JSON strings
            resume.skills = json.dumps(skills) if skills else None
            resume.experience = json.dumps(experience) if experience else None
            resume.education = json.dumps(education) if education else None
            
            # If a job is associated, calculate similarity score
            if resume.job_id:
                job = Job.query.get(resume.job_id)
                if job:
                    job_text = f"{job.title} {job.description} {job.requirements}"
                    resume.score = calculate_similarity(text, job_text)
                    
                    # Extract keywords from job description
                    job_keywords = extract_skills(job_text)
                    
                    # Find matched and missing keywords
                    matched_keywords = [skill for skill in skills if skill in job_keywords]
                    missing_keywords = [skill for skill in job_keywords if skill not in skills]
                    
                    resume.matched_keywords = json.dumps(matched_keywords) if matched_keywords else None
                    resume.missing_keywords = json.dumps(missing_keywords) if missing_keywords else None
            
            # Update status to processed
            resume.status = 'processed'
            db.session.commit()
            
        except Exception as e:
            current_app.logger.error(f"Error processing resume {resume_id}: {str(e)}")
            if 'resume' in locals():
                resume.status = 'error'
                db.session.commit()

def export_resumes_to_excel(job_id=None, output_path=None):
    """Export resumes data to an Excel file."""
    try:
        # Query resumes
        query = Resume.query
        if job_id:
            query = query.filter_by(job_id=job_id)
        
        resumes = query.all()
        
        # Prepare data for DataFrame
        data = []
        for resume in resumes:
            skills = json.loads(resume.skills) if resume.skills else []
            experience = json.loads(resume.experience) if resume.experience else {}
            education = json.loads(resume.education) if resume.education else {}
            matched_keywords = json.loads(resume.matched_keywords) if resume.matched_keywords else []
            missing_keywords = json.loads(resume.missing_keywords) if resume.missing_keywords else []
            
            data.append({
                'ID': resume.id,
                'Name': resume.name or 'N/A',
                'Email': resume.email or 'N/A',
                'Phone': resume.phone or 'N/A',
                'Filename': resume.original_filename,
                'Upload Date': resume.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
                'Score': f"{resume.score}%" if resume.score is not None else 'N/A',
                'Skills': ', '.join(skills) if skills else 'N/A',
                'Experience': json.dumps(experience, indent=2) if experience else 'N/A',
                'Education': json.dumps(education, indent=2) if education else 'N/A',
                'Matched Keywords': ', '.join(matched_keywords) if matched_keywords else 'N/A',
                'Missing Keywords': ', '.join(missing_keywords) if missing_keywords else 'N/A',
                'Status': resume.status.capitalize()
            })
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # If no output path provided, create one in the temp directory
        if not output_path:
            filename = f"resumes_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            output_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'exports', filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Export to Excel
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        return output_path
    
    except Exception as e:
        current_app.logger.error(f"Error exporting resumes to Excel: {str(e)}")
        raise

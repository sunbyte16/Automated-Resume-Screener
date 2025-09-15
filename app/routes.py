from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import os
import uuid
from .models import db, Resume, Job
from .utils import allowed_file, process_resume

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page with resume upload form."""
    jobs = Job.query.filter_by(is_active=True).all()
    return render_template('index.html', jobs=jobs)

@main.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """
    Handle file upload and process resume.
    Accepts PDF and DOCX files.
    """
    if 'resume' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    
    file = request.files['resume']
    
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(filepath)
        
        # Create resume record
        resume = Resume(
            filename=unique_filename,
            file_path=filepath,
            original_filename=filename,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        
        db.session.add(resume)
        db.session.commit()
        
        # Process resume in background
        process_resume(resume.id)
        
        flash('Resume uploaded successfully!', 'success')
        return redirect(url_for('main.view_resume', resume_id=resume.id))
    
    flash('Invalid file type. Please upload a PDF or DOCX file.', 'error')
    return redirect(url_for('main.index'))

@main.route('/resume/<int:resume_id>')
@login_required
def view_resume(resume_id):
    """View details of a specific resume."""
    resume = Resume.query.get_or_404(resume_id)
    
    # Only allow resume owner or admin to view
    if not current_user.is_admin and (not current_user.is_authenticated or resume.user_id != current_user.id):
        flash('You do not have permission to view this resume.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('view_resume.html', resume=resume)

@main.route('/api/resumes')
@login_required
def get_resumes():
    """API endpoint to get all resumes for the current user."""
    if current_user.is_admin:
        resumes = Resume.query.all()
    else:
        resumes = Resume.query.filter_by(user_id=current_user.id).all()
    
    return jsonify([{
        'id': r.id,
        'filename': r.original_filename,
        'upload_date': r.upload_date.isoformat(),
        'status': r.status,
        'score': r.score
    } for r in resumes])

@main.route('/jobs')
def list_jobs():
    """List all active job postings."""
    jobs = Job.query.filter_by(is_active=True).all()
    return render_template('jobs.html', jobs=jobs)

@main.route('/job/<int:job_id>')
def view_job(job_id):
    """View details of a specific job posting."""
    job = Job.query.get_or_404(job_id)
    return render_template('job_detail.html', job=job)

@main.route('/profile')
@login_required
def profile():
    """User profile page."""
    return render_template('profile.html', user=current_user)

@main.route('/download/<int:resume_id>')
@login_required
def download_resume(resume_id):
    """Download a resume file."""
    resume = Resume.query.get_or_404(resume_id)
    
    # Check permissions
    if not current_user.is_admin and resume.user_id != current_user.id:
        flash('You do not have permission to download this resume.', 'error')
        return redirect(url_for('main.index'))
    
    directory = os.path.dirname(resume.file_path)
    filename = os.path.basename(resume.file_path)
    
    return send_from_directory(
        directory=directory,
        path=filename,
        as_attachment=True,
        download_name=resume.original_filename
    )

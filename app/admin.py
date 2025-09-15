from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from .models import Resume, Job, User
from .forms import JobForm
import os

admin = Blueprint('admin', __name__)

@admin.before_request
@login_required
def require_admin():
    """Ensure only admin users can access admin routes."""
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('main.index'))

@admin.route('/')
@login_required
def dashboard():
    """Admin dashboard with statistics."""
    stats = {
        'total_resumes': Resume.query.count(),
        'total_jobs': Job.query.count(),
        'total_users': User.query.count(),
        'pending_resumes': Resume.query.filter_by(status='pending').count(),
    }
    
    recent_resumes = Resume.query.order_by(Resume.upload_date.desc()).limit(5).all()
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_resumes=recent_resumes,
                         recent_jobs=recent_jobs)

@admin.route('/resumes')
@login_required
def manage_resumes():
    """View and manage all resumes."""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    query = Resume.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    resumes = query.order_by(Resume.upload_date.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/resumes.html', 
                         resumes=resumes,
                         current_status=status)

@admin.route('/resume/<int:resume_id>/delete', methods=['POST'])
@login_required
def delete_resume(resume_id):
    """Delete a resume."""
    resume = Resume.query.get_or_404(resume_id)
    
    # Delete the file
    try:
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'error')
    
    # Delete the database record
    db.session.delete(resume)
    db.session.commit()
    
    flash('Resume deleted successfully!', 'success')
    return redirect(url_for('admin.manage_resumes'))

@admin.route('/resume/<int:resume_id>/download')
@login_required
def download_resume(resume_id):
    """Download a resume file."""
    resume = Resume.query.get_or_404(resume_id)
    directory = os.path.dirname(resume.file_path)
    filename = os.path.basename(resume.file_path)
    
    return send_from_directory(
        directory=directory,
        path=filename,
        as_attachment=True,
        download_name=resume.original_filename
    )

@admin.route('/jobs')
@login_required
def manage_jobs():
    """View and manage all job postings."""
    jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('admin/jobs.html', jobs=jobs)

@admin.route('/job/new', methods=['GET', 'POST'])
@login_required
def new_job():
    """Create a new job posting."""
    form = JobForm()
    
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            description=form.description.data,
            requirements=form.requirements.data
        )
        
        db.session.add(job)
        db.session.commit()
        
        flash('Job posting created successfully!', 'success')
        return redirect(url_for('admin.manage_jobs'))
    
    return render_template('admin/job_form.html', form=form, title='New Job Posting')

@admin.route('/job/create', methods=['GET', 'POST'])
@login_required
def create_job():
    """Create a new job posting (alias for new_job)."""
    return new_job()

@admin.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    """Edit an existing job posting."""
    job = Job.query.get_or_404(job_id)
    form = JobForm(obj=job)
    
    if form.validate_on_submit():
        job.title = form.title.data
        job.description = form.description.data
        job.requirements = form.requirements.data
        
        db.session.commit()
        
        flash('Job posting updated successfully!', 'success')
        return redirect(url_for('admin.manage_jobs'))
    
    return render_template('admin/job_form.html', form=form, title='Edit Job Posting')

@admin.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    """Delete a job posting."""
    job = Job.query.get_or_404(job_id)
    
    # Update related resumes to remove job association
    Resume.query.filter_by(job_id=job_id).update({Resume.job_id: None})
    
    db.session.delete(job)
    db.session.commit()
    
    flash('Job posting deleted successfully!', 'success')
    return redirect(url_for('admin.manage_jobs'))

@admin.route('/job/<int:job_id>/toggle', methods=['POST'])
@login_required
def toggle_job(job_id):
    """Toggle job posting status (active/inactive)."""
    job = Job.query.get_or_404(job_id)
    job.is_active = not job.is_active
    
    db.session.commit()
    
    status = 'activated' if job.is_active else 'deactivated'
    flash(f'Job posting {status} successfully!', 'success')
    return redirect(url_for('admin.manage_jobs'))

@admin.route('/users')
@login_required
def manage_users():
    """View and manage all users."""
    users = User.query.order_by(User.username).all()
    return render_template('admin/users.html', users=users)

@admin.route('/user/<int:user_id>/toggle_admin', methods=['POST'])
@login_required
def toggle_admin(user_id):
    """Toggle admin status for a user."""
    if user_id == current_user.id:
        flash('You cannot modify your own admin status.', 'error')
        return redirect(url_for('admin.manage_users'))
    
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    
    db.session.commit()
    
    status = 'granted' if user.is_admin else 'revoked'
    flash(f'Admin privileges {status} for user {user.username}.', 'success')
    return redirect(url_for('admin.manage_users'))

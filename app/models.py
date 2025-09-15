from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class User(UserMixin, db.Model):
    """User model for authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)

class Resume(db.Model):
    """Resume model to store resume information."""
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, processed, error
    
    # Extracted information
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    skills = db.Column(db.Text)  # JSON string of skills
    experience = db.Column(db.Text)  # JSON string of experience
    education = db.Column(db.Text)  # JSON string of education
    
    # Scoring
    score = db.Column(db.Float, default=0.0)
    matched_keywords = db.Column(db.Text)  # JSON string of matched keywords
    missing_keywords = db.Column(db.Text)  # JSON string of missing keywords
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    
    def __repr__(self):
        return f'<Resume {self.filename}>'

class Job(db.Model):
    """Job description model."""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)  # JSON string of required skills/qualifications
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    resumes = db.relationship('Resume', backref='job', lazy=True)
    
    def __repr__(self):
        return f'<Job {self.title}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

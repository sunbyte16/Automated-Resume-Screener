#!/usr/bin/env python3
"""
Setup script for Automated Resume Screener
This script helps set up the application for first-time users.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories."""
    directories = [
        "app/static/uploads",
        "app/static/uploads/exports",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# Flask Configuration
SECRET_KEY=dev-key-for-testing-change-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
SQLALCHEMY_DATABASE_URI=sqlite:///resume_screener.db

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
UPLOAD_FOLDER=app/static/uploads

# Security
WTF_CSRF_ENABLED=True
WTF_CSRF_TIME_LIMIT=3600
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("📝 Created .env file with default configuration")
    else:
        print("📝 .env file already exists")

def create_admin_user():
    """Create an admin user for initial setup."""
    try:
        from app import create_app, db
        from app.models import User
        
        app = create_app()
        with app.app_context():
            # Check if admin user already exists
            admin = User.query.filter_by(is_admin=True).first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    is_admin=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("👤 Created default admin user:")
                print("   Username: admin")
                print("   Email: admin@example.com")
                print("   Password: admin123")
                print("   ⚠️  Please change these credentials after first login!")
            else:
                print("👤 Admin user already exists")
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")

def main():
    """Main setup function."""
    print("🚀 Setting up Automated Resume Screener...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Download spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy language model"):
        print("❌ Failed to download spaCy model. You may need to install it manually.")
    
    # Create admin user
    create_admin_user()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the application: python run.py")
    print("2. Open your browser: http://localhost:5000")
    print("3. Login with admin credentials (change them after first login)")
    print("4. Start uploading resumes and creating job postings!")
    print("\n📚 For more information, see the README.md file")

if __name__ == "__main__":
    main()

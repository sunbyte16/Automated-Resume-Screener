import os
from app import create_app, db
from app.models import User, Resume, Job

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Resume': Resume, 'Job': Job}

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Create exports directory if it doesn't exist
    export_dir = os.path.join(upload_dir, 'exports')
    os.makedirs(export_dir, exist_ok=True)
    
    app.run(debug=True)

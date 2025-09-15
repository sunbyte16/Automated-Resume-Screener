#!/usr/bin/env python3
"""
Test script to verify the Automated Resume Screener setup
"""

import sys
import os
import importlib

def test_imports():
    """Test if all required modules can be imported."""
    required_modules = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_wtf',
        'werkzeug',
        'PyPDF2',
        'docx',
        'spacy',
        'sklearn',
        'pandas',
        'openpyxl'
    ]
    
    print("🔍 Testing module imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_spacy_model():
    """Test if spaCy English model is available."""
    print("\n🔍 Testing spaCy model...")
    try:
        import spacy
        nlp = spacy.load('en_core_web_sm')
        print("✅ spaCy English model loaded successfully")
        return True
    except OSError as e:
        print(f"❌ spaCy model not found: {e}")
        print("   Run: python -m spacy download en_core_web_sm")
        return False

def test_app_creation():
    """Test if the Flask app can be created."""
    print("\n🔍 Testing Flask app creation...")
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create Flask app: {e}")
        return False

def test_database():
    """Test database connection and table creation."""
    print("\n🔍 Testing database...")
    try:
        from app import create_app, db
        from app.models import User, Resume, Job
        
        app = create_app()
        with app.app_context():
            # Test database connection
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Test model creation
            user = User(username='test', email='test@example.com')
            user.set_password('test123')
            print("✅ User model works correctly")
            
            return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_file_processing():
    """Test file processing utilities."""
    print("\n🔍 Testing file processing utilities...")
    try:
        from app.utils import allowed_file, extract_text_from_pdf, extract_text_from_docx
        
        # Test allowed_file function
        assert allowed_file('test.pdf') == True
        assert allowed_file('test.docx') == True
        assert allowed_file('test.txt') == False
        print("✅ File validation works correctly")
        
        return True
    except Exception as e:
        print(f"❌ File processing test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Automated Resume Screener Setup")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("spaCy Model", test_spacy_model),
        ("Flask App", test_app_creation),
        ("Database", test_database),
        ("File Processing", test_file_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

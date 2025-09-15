from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User

class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Check if username is already in use."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Check if email is already in use."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class JobForm(FlaskForm):
    """Form for creating/editing job postings."""
    title = StringField('Job Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Job Description', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    submit = SubmitField('Save')

class ResumeUploadForm(FlaskForm):
    """Form for uploading resumes."""
    resume = FileField('Upload Resume', validators=[DataRequired()])
    job_id = SelectField('Job Position', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Upload & Process')
    
    def __init__(self, *args, **kwargs):
        super(ResumeUploadForm, self).__init__(*args, **kwargs)
        # Populate job choices from the database
        from .models import Job
        self.job_id.choices = [(job.id, job.title) for job in Job.query.filter_by(is_active=True).order_by(Job.title).all()]
        self.job_id.choices.insert(0, (0, 'Select a job position...'))

class SearchForm(FlaskForm):
    """Form for searching resumes."""
    query = StringField('Search', validators=[Length(min=0, max=200)])
    min_score = SelectField('Minimum Score', 
                          choices=[(str(i), f'{i}%') for i in range(0, 101, 10)],
                          default='0')
    skills = StringField('Skills (comma-separated)')
    submit = SubmitField('Search')

class ProfileForm(FlaskForm):
    """Form for user profile updates."""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[
        Length(min=0, max=128),  # Optional field
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm New Password')
    submit = SubmitField('Update Profile')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        """Check if username is already in use."""
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        """Check if email is already in use."""
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

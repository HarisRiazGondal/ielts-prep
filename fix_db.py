import os
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Create a base class for declarative models
class Base(DeclarativeBase):
    pass

# Create SQLAlchemy instance
db = SQLAlchemy(model_class=Base)

# Create Flask application
app = Flask(__name__)

# Configure database to use an absolute path for SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'ielts_prep.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)  # Ensure instance directory exists

# Configure app
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("SESSION_SECRET", os.urandom(24))

# Initialize db with app
db.init_app(app)

# Import models to register with SQLAlchemy
with app.app_context():
    from models import User, Role, Section, Difficulty, Exercise, PracticeRecord, Score, Badge, UserBadge
    
    # Create all tables
    db.create_all()
    
    # Populate initial data
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator')
        db.session.add(admin_role)
    
    student_role = Role.query.filter_by(name='student').first()
    if not student_role:
        student_role = Role(name='student', description='Student')
        db.session.add(student_role)
    
    db.session.commit()
    
    from werkzeug.security import generate_password_hash
    admin_user = User.query.filter_by(email='admin@ieltsapp.com').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@ieltsapp.com',
            password_hash=generate_password_hash('admin123'),
            role_id=admin_role.id
        )
        db.session.add(admin_user)
    
    # Add exam sections if they don't exist
    sections = ['Reading', 'Writing', 'Listening', 'Speaking']
    for section_name in sections:
        section = Section.query.filter_by(name=section_name).first()
        if not section:
            section = Section(name=section_name, description=f'{section_name} section of the IELTS exam')
            db.session.add(section)
    
    # Add difficulty levels if they don't exist
    difficulties = ['Beginner', 'Intermediate', 'Advanced']
    for diff_name in difficulties:
        difficulty = Difficulty.query.filter_by(name=diff_name).first()
        if not difficulty:
            difficulty = Difficulty(name=diff_name, description=f'{diff_name} difficulty level')
            db.session.add(difficulty)
    
    db.session.commit()
    
    print("Database initialized successfully!")
    print(f"Database path: {db_path}")
    print("Admin credentials: admin@ieltsapp.com / admin123")

if __name__ == "__main__":
    print("Script completed.") 
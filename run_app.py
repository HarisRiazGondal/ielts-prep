import os
import logging
from app import create_app

# Determine environment
env = os.environ.get('FLASK_ENV', 'development')

# Configure base directory and database path
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'ielts_prep.db')

# Create app with configuration
app = create_app()

# Override database configuration
if env == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['DEBUG'] = True
elif env == 'testing':
    test_db_path = os.path.join(basedir, 'instance', 'test_db.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{test_db_path}"
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
elif env == 'production':
    # Use environment variables for production database
    db_uri = os.environ.get('DATABASE_URL', f"sqlite:///{db_path}")
    
    # Handle Heroku's postgres:// vs postgresql:// URL scheme
    if db_uri.startswith('postgres://'):
        db_uri = db_uri.replace('postgres://', 'postgresql://', 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['DEBUG'] = False
    
    # Enable HTTPS only cookies in production
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True

# Configure logging based on environment
if env == 'production':
    app.logger.setLevel(logging.INFO)
else:
    app.logger.setLevel(logging.DEBUG)

# Run the application
if __name__ == '__main__':
    print("IELTS Preparation App is starting...")
    print(f"Environment: {env}")
    print(f"Database path: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("Admin credentials: admin@ieltsapp.com / admin123")
    print("Access the application at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG']) 
import os
import logging
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from flask_migrate import Migrate

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='config.Config'):
    """Factory function to create and configure the Flask application"""
    app = Flask(__name__)
    
    # Determine config class based on environment
    if isinstance(config_name, str):
        if config_name == 'config.Config':
            env = os.environ.get('FLASK_ENV', 'development').lower()
            if env == 'production':
                config_name = 'config.ProductionConfig'
            elif env == 'testing':
                config_name = 'config.TestingConfig'
            else:
                config_name = 'config.DevelopmentConfig'
    
    # Load configuration
    app.config.from_object(config_name)
    
    # Set secret key from environment variable or use a random one
    app.secret_key = os.environ.get("SESSION_SECRET", os.urandom(24))
    
    # Configure file uploads
    app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30MB limit for audio files
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    
    # Create upload directories if they don't exist
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'audio'), exist_ok=True)
    
    # Apply ProxyFix middleware for handling reverse proxies
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize database with the app
    db.init_app(app)
    
    # Initialize database migrations
    migrate.init_app(app, db)
    
    # Register asset management
    from asset_utils import AssetManager
    AssetManager.register_asset_helpers(app)
    
    # Add custom Jinja2 filters
    @app.template_filter('strftime')
    def _jinja2_filter_strftime(date, fmt=None):
        if fmt is None:
            fmt = '%Y-%m-%d'
        return date.strftime(fmt) if date else ''
    
    @app.template_filter('from_json')
    def _jinja2_filter_from_json(value):
        import json
        try:
            if isinstance(value, str):
                return json.loads(value)
            return value
        except (ValueError, TypeError):
            app.logger.error(f"Error parsing JSON: {value[:100]}")
            return {}
    
    # Initialize and configure LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.student import student_bp
    from routes.practice import practice_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(practice_bp, url_prefix='/practice')
    
    # Register error handlers
    from error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Default route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Initialize database tables
    with app.app_context():
        _initialize_database()
    
    # Call init_app on config if it exists (for env-specific setup)
    if hasattr(app.config, 'init_app'):
        app.config.init_app(app)
    
    return app

def _initialize_database():
    """Initialize database tables and set up initial data"""
    import models  # Import models to register them with SQLAlchemy
    db.create_all()
    
    # Create admin user if it doesn't exist
    from models import User, Role
    from werkzeug.security import generate_password_hash
    
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator')
        db.session.add(admin_role)
    
    student_role = Role.query.filter_by(name='student').first()
    if not student_role:
        student_role = Role(name='student', description='Student')
        db.session.add(student_role)
    
    db.session.commit()
    
    admin_user = User.query.filter_by(email='admin@ieltsapp.com').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@ieltsapp.com',
            password_hash=generate_password_hash('admin123'),
            role_id=admin_role.id
        )
        db.session.add(admin_user)
        db.session.commit()
        logger.info("Admin user created successfully")

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Create the application instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

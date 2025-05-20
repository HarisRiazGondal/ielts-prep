import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Base configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'instance/ielts_prep.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.environ.get('DB_POOL_SIZE', 10)),
        'pool_recycle': 3600,  # Recycle connections after 1 hour
        'pool_pre_ping': True,  # Test connections before using them
        'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', 20)),
    }
    
    # Upload configuration
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB file size limit
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
    ALLOWED_EXTENSIONS = {
        'image': ['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'],
        'audio': ['mp3', 'wav', 'ogg', 'm4a'],
        'document': ['pdf', 'doc', 'docx', 'txt']
    }
    
    # Cache configuration
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 3600  # 1 hour
    STATIC_CACHE_TIMEOUT = 2592000  # 30 days for static assets
    
    # Debug configuration
    DEBUG = False
    TESTING = False
    
    # Security configuration
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() in ('true', 'yes', 't', 'y', '1')
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = os.environ.get('REMEMBER_COOKIE_SECURE', 'False').lower() in ('true', 'yes', 't', 'y', '1')
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Asset Management
    ASSET_VERSIONING = True
    ASSET_VERSION = os.environ.get('ASSET_VERSION', '1.0')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_pre_ping': True,
    }
    CACHE_TYPE = 'NullCache'  # Disable caching in development

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    SERVER_NAME = 'localhost:5000'
    WTF_CSRF_ENABLED = False
    CACHE_TYPE = 'NullCache'  # Disable caching in tests

class ProductionConfig(Config):
    # Production specific settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
    # Use Redis for session/cache if available
    if os.environ.get('REDIS_URL'):
        SESSION_TYPE = 'redis'
        CACHE_TYPE = 'RedisCache'
        CACHE_REDIS_URL = os.environ.get('REDIS_URL')
        
    # Enable file logging
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT', 'False').lower() in ('true', 'yes', 't', 'y', '1')
    
    # CDN configuration if available
    CDN_DOMAIN = os.environ.get('CDN_DOMAIN')
    
    @classmethod
    def init_app(cls, app):
        # Set up production-specific handlers
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Configure production logging
        if not cls.LOG_TO_STDOUT:
            file_handler = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('StudentExamPrep startup')

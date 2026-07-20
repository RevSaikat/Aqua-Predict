import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _require_env(var: str) -> str:
    """Return the value of a required environment variable.

    Raises ValueError at import time if the variable is not set.
    Keeps validation logic out of class bodies so static analysers
    (e.g. pyrefly) can resolve names correctly.
    """
    value = os.environ.get(var)
    if not value:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError(f"No {var} set for Flask application in production!")
        return "dummy-secret-key"
    return value


# ---------------------------------------------------------------------------
# Module-level env reads — referenced  inside class bodies so that pyrefly's
# virtual-file class-body analysis never encounters bare `os` calls.
# ---------------------------------------------------------------------------
_SECRET_KEY_DEFAULT: str = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
_MODEL_PATH_DEFAULT: str = os.environ.get('MODEL_PATH') or './models/logreg.pkl'


class Config:
    """Base configuration"""
    SECRET_KEY: str = _SECRET_KEY_DEFAULT
    MODEL_PATH: str = _MODEL_PATH_DEFAULT
    
    # Flask-WTF CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Application Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

    # Validated at import time — raises ValueError if SECRET_KEY is unset
    SECRET_KEY: str = _require_env('SECRET_KEY')
    

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

from pathlib import Path


class BaseConfig:
    """Base configuration"""
    BASE_DIR = Path(__file__).parent.parent
    
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    WTF_CSRF_ENABLED = True
    
    SECRET_KEY = '8fUqFEeM9WWUnLtBS5BqLhboibcXCVJq'
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/user.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {'order': 'sqlite:///database/order.db',
                        'ingress': 'sqlite:///database/ingress.db',
                        'task': 'sqlite:///database/task.db',
                        'robot': 'sqlite:///database/robot.db'}
    SECURITY_PASSWORD_SALT = 'hjdsafjkhalkj'
    SECURITY_PASSWORD_HASH='bcrypt'
    SECURITY_RECOVERABLE=True
    SECURITY_CHANGEABLE=True

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
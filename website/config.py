"""Configuration objects for Flask app."""


class BaseSettings(object):
    """Base app settings."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "s3cr3t"


class DevSettings(BaseSettings):
    """App development settings."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = 'development'
    DEBUG = True


class TestSettings(BaseSettings):
    """App test settings."""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """ Base config """
    SECRET_KEY = environ.get("SECRET_KEY")
    ORG_NAME = environ.get("ORG_NAME")
    API_TOKEN = environ.get("API_TOKEN")
    ISSUER = environ.get("ISSUER")
    AUDIENCE = environ.get("AUDIENCE")
    CACHE_METHOD = environ.get("CACHE_METHOD", "file")
    BUCKET_NAME = environ.get("S3_BUCKET", None)


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    LOG_LEVEL = environ.get("LOG_LEVEL", "WARNING")


class DevConfig(Config):
    # flask settings
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    LOG_LEVEL = environ.get("LOG_LEVEL", "DEBUG")

import os
from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """ Base config """
    SECRET_KEY = os.getenv("SECRET_KEY")
    ORG_NAME = os.getenv("ORG_NAME")
    API_TOKEN = os.getenv("API_TOKEN")
    ISSUER = os.getenv("ISSUER")
    AUDIENCE = os.getenv("AUDIENCE")
    CACHE_METHOD = os.getenv("CACHE_METHOD", "file")
    BUCKET_NAME = os.getenv("S3_BUCKET", None)


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

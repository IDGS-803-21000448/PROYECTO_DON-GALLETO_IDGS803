import os
from sqlalchemy import create_engine
import urllib

class Config(object):
    SECRET_KEY = 'mi clave secreta'
    SESION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://donGalleto:1234@127.0.0.1/proyecto_don_galleto'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

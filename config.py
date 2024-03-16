import os
from sqlalchemy import create_engine
import urllib

class Config(object):
    SECRET_KEY = 'mi clave secreta'
    SESION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://carlos:123456@127.0.0.1/practicas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


from encryption import cargar_clave, desencriptar_texto
import os
from sqlalchemy import create_engine
import urllib

class Config(object):
    SECRET_KEY = 'mi clave secreta'
    SESION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = desencriptar_texto('gAAAAABmEz2iXfDs-yEA5iq0SjgaEs1reIkq4BkyVNWVtaQ2kkX55Zi5_NnUbiOgIHlC-Qdj-uea4-AiqDzuzulf8NLYJuOp1RuQS1tZBaRkWVG0p17DCAjq1fnXlKix_cT6QqrvjSxE-6PDUyOD2Tstcg7E8sbOEw==')
    SQLALCHEMY_TRACK_MODIFICATIONS = False



# import os
# from sqlalchemy import create_engine
# import urllib

# class Config(object):
#     SECRET_KEY = 'mi clave secreta'
#     SESION_COOKIE_SECURE = False

# class DevelopmentConfig(Config):
#     DEBUG = True
#     FLASK_ENV = 'development'
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://donGalleto:1234@127.0.0.1/proyecto_don_galleto'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


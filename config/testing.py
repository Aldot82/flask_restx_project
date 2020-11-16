from .default import *
import os


user = os.getenv('MYSQL_USER_TEST')
pasw = os.getenv('MYSQL_PASSWORD_TEST')
name = os.getenv('MYSQL_DATABASE_TEST')
host = os.getenv('MYSQL_HOST_TEST')

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_TESTING')
TESTING = True
DEBUG = True
APP_ENV = APP_ENV_TESTING
WTF_CSRF_ENABLED = False

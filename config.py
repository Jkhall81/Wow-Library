import secrets
import os

file_path = os.path.abspath(os.getcwd()) + '/data/library.sqlite'
secret_key = secrets.token_hex(16)
# DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + file_path
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = secret_key
CACHE_TYPE = 'simple'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

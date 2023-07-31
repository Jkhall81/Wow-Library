import secrets

secret_key = secrets.token_hex(16)
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/library.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = secret_key
CACHE_TYPE = 'simple'

import os


basedir = os.path.abspath(os.path.dirname(__file__))
DEBAG = True
PORT = 5000
HOST = '127.0.0.1'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = os.environ.get('MESSAGES_DB_URL')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

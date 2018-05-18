import os


basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
PORT = 5000
HOST = '127.0.0.1'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "{0}{1}".format(os.environ.get('MESSAGES_DB_URL'),
                                          "test_messages")
TESTING = True
SERVER_NAME = '127.0.0.1:5000'                        
PAGINATION_PAGE_SIZE = 5
PAGINATION_PAGE_ARGUMENT_NAME = 'page'
WTF_CSRF_ENABLED = False
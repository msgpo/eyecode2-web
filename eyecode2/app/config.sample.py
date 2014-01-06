import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = False

ADMINS = frozenset(['user@domain.com'])
SECRET_KEY = 'secret1'

BASIC_AUTH_USERNAME = "admin"
BASIC_AUTH_PASSWORD = "secret potato pocket"

SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@server/database'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED=True
CSRF_SESSION_KEY="secret2"

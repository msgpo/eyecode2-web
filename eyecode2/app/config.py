import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TESTING = True

ADMINS = frozenset(['mihansen@indiana.edu'])
SECRET_KEY = 'cudr6tacasWeStekafegerehu'

BASIC_AUTH_USERNAME = "hansenm"
BASIC_AUTH_PASSWORD = "grover"

SQLALCHEMY_DATABASE_URI = 'mysql://eyecode_user:bARutH7ph3QAdrU@mysql.synesthesiam.com/eyecode2'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

CSRF_ENABLED=True
CSRF_SESSION_KEY="NezasPe6Ud68paTHAResAsW4q"

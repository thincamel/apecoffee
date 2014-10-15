# -*- coding: utf8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

# email server
MAIL_SERVER = '' # your mailserver
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'you'
MAIL_PASSWORD = 'your-password'

# available languages
LANGUAGES = {
    'en': 'English',
    'zh': 'Chinese'
}


# administrator list
ADMINS = ['info@99party.com']

# pagination
COUNT_PER_PAGE = 11
MAX_SEARCH_RESULTS = 50

# security
SECRET_KEY = 'its a dog'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha256'
SECURITY_PASSWORD_SALT = 'so-salty'
SECURITY_CHANGEABLE = 0
SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'
SECURITY_REGISTER_USER_TEMPLATE = 'security/register.html'
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False

#Debug Toolbar
DEBUG_TB_INTERCEPT_REDIRECTS=False


#Search Engine
WHOOSH_BASE = os.path.join(basedir, 'search.db')
# config.py

import os

class Config:
    # Flask’s secret key for signing sessions + CSRF tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-should-never-use-this-default'
    WTF_CSRF_ENABLED = True

    SESSION_COOKIE_SECURE   = True       # only send cookies over HTTPS
    SESSION_COOKIE_HTTPONLY = True       # JS can’t read the cookie
    SESSION_COOKIE_SAMESITE = 'Lax'      # mitigate CSRF via cross-site contexts
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production' # only send cookies over HTTPS in production
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # cache static files for 1 year
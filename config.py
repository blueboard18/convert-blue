# config.py

import os

class Config:
    # Flask’s secret key for signing sessions + CSRF tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-should-never-use-this-default'

    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'

    # Restrict cross-site sending of cookies; 'Lax' prevents CSRF in most cases
    SESSION_COOKIE_SAMESITE = 'Lax'

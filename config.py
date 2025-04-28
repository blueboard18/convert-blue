# config.py

import os

class Config:
    # Flask’s secret key for signing sessions + CSRF tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-should-never-use-this-default'

    # Only send the session cookie over HTTPS
    SESSION_COOKIE_SECURE   = True
    # Make session cookie inaccessible to JavaScript
    SESSION_COOKIE_HTTPONLY = True
    # Restrict cross-site sending of cookies; 'Lax' prevents CSRF in most cases
    SESSION_COOKIE_SAMESITE = 'Lax'

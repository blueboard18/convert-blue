from flask import Flask
from flask_compress import Compress
from flask_assets import Environment, Bundle
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from config import Config
import os
from flask_wtf.csrf import CSRFProtect
import base64


csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=["200/hour"])

def create_app():
    app = Flask(__name__)
    sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN"), integrations=[FlaskIntegration()])
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Set cache control for static files
    app.config.from_object(Config)
    Compress(app)  # <-- enables Gzip/Brotli on responses
    csrf.init_app(app)     # ← registers CSRF checks on all POST/PUT/DELETE
    limiter.init_app(app)

    # Register Jinja filter for base64 encoding
    @app.template_filter('b64encode')
    def b64encode_filter(data):
        return base64.b64encode(data).decode('utf-8')

    # —— Assets setup ——
    assets = Environment(app)

    # CSS bundle: style.css → gen/style.min.css
    css_bundle = Bundle(
        'style.css',
        filters='cssmin',
        output='gen/style.min.css'
    )
    assets.register('all_css', css_bundle)

    # build bundles at startup (or you can run `flask assets build` in a script)
    css_bundle.build()

    from .routes import main
    app.register_blueprint(main)

        # —— PUT HSTS HERE ——
    @app.after_request
    def set_hsts(response):
        # tell browsers to always use HTTPS for next 365 days
        response.headers['Strict-Transport-Security'] = \
          'max-age=31536000; includeSubDomains; preload'
        return response
    

    # only enforce HTTPS (and HSTS) when running in production
    if os.environ.get('FLASK_ENV') == 'production':
        Talisman(app,
            force_https=True,
            content_security_policy={
                "default-src": ["'self'"],
                "script-src":  ["'self'", "'unsafe-inline'"],
                "style-src":   ["'self'"],
            }
        )

    return app

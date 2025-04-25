from flask import Flask
from flask_compress import Compress
from flask_assets import Environment, Bundle



def create_app():
    app = Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Set cache control for static files
    app.config.from_envvar('APP_SETTINGS', silent=True)  # Load environment-specific settings if available
    Compress(app)  # <-- enables Gzip/Brotli on responses

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

    return app

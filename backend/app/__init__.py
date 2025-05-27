from flask import Flask
from .routes.status import status_bp
from .routes.csv_upload import csv_upload_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(status_bp, url_prefix="/api")
    app.register_blueprint(csv_upload_bp, url_prefix="/api")

    return app

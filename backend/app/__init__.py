from flask import Flask
from app.routes.sensor_data import sensor_bp
from app.routes.key_share import key_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(sensor_bp)
    app.register_blueprint(key_bp)
    return app

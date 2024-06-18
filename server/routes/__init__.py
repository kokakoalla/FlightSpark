from flask import Flask
from .location import location_bp
from .flight import flight_bp
from .radius import radius_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(location_bp)
    app.register_blueprint(flight_bp)
    app.register_blueprint(radius_bp)
    return app

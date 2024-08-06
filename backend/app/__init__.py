from flask import Flask
from flask_cors import CORS
from .config import Config
#from .extensions import db
from .api.routes import api_bp  # Update this line

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    #db.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
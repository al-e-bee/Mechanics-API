from flask import Flask
from .extensions import ma # Relative import
from .models import db
from .blueprints.customers import customers_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    # initialize extensions
    ma.init_app(app)
    db.init_app(app)
    
    # Register Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    
    
    return app

# App Factory Function : creates and returns Flask apps
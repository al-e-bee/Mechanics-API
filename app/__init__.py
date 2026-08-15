from flask import Flask
from .extensions import ma, limiter, cache # Relative import
from .models import db
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint 


SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanics API Documentation"
    }
)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    # initialize extensions
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    # Register Blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')
    
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    
    # Register Swagger Blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    return app

# App Factory Function : creates and returns Flask apps
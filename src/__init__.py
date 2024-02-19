from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost"}})

db = MySQL(app)

def init_app(config):
    
    # Routes
    from .routes import AuthRoutes, ProductRoutes
    
    # Configuration
    app.config.from_object(config)
    
    app.register_blueprint(AuthRoutes.auth, url_prefix='/api/auth')
    app.register_blueprint(ProductRoutes.product, url_prefix='/api/product')
    
    return app

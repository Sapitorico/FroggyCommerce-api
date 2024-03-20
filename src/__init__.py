from flask import Flask
from flask_cors import CORS

# Routes
from .routes import AuthRoutes, ProductRoutes, UserRoutes, CartRoutes, AddressRoutes, PaymentRoutes


app = Flask(__name__)

# Configuring CORS to allow requests
CORS(app, resources={r"/api/*": {"origins": "http://localhost"}})


def init_app(config):
    """
    Function to initialize the application with a specific configuration
    """

    # Configuration
    app.config.from_object(config)

    # Registering authentication routes
    app.register_blueprint(AuthRoutes.auth, url_prefix='/api/auth')
    # Registering users routes
    app.register_blueprint(UserRoutes.user, url_prefix='/api/users')
    # Registering products routes
    app.register_blueprint(ProductRoutes.product, url_prefix='/api/products')
    # Registering cart routes
    app.register_blueprint(CartRoutes.cart, url_prefix='/api/cart')
    # Registering address routes
    app.register_blueprint(AddressRoutes.address, url_prefix='/api/address')
    # register payment routes
    app.register_blueprint(PaymentRoutes.payment, url_prefix='/api/payment')
    
    return app

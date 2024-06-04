import os
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

# Routes
from .routes import AuthRoutes, CartRoutes, AddressRoutes, PaymentRoutes, ProductsRoutes, CategoriesRoutes, UsersRoutes, ReviewsRoutes

SWAGGER_URL = "/api"
API_URL = "/static/openapi.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'FroggyCommerce'
    }
)

app = Flask(__name__)

# Configuring CORS to allow requests
CORS(app, resources={r"/api/*": {"origins": "http://localhost"}})


def init_app(config):
    """
    Function to initialize the application with a specific configuration
    """

    # Configuration
    env = os.getenv('ENV', 'development')
    if env == 'production':
        app.config.from_object(config['production'])
    else:
        app.config.from_object(config['development'])

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # Registering authentication routes
    app.register_blueprint(AuthRoutes.auth, url_prefix='/api/auth')
    # Registering users routes
    app.register_blueprint(UsersRoutes.user, url_prefix='/api/users')
    # Registering products routes
    app.register_blueprint(ProductsRoutes.product, url_prefix='/api/products')
    # Registering categories routes
    app.register_blueprint(CategoriesRoutes.categories,
                           url_prefix='/api/categories')
    # Registering cart routes
    app.register_blueprint(CartRoutes.cart, url_prefix='/api/cart')
    # Registering reviews routes
    app.register_blueprint(ReviewsRoutes.reviews, url_prefix='/api/reviews')
    # Registering address routes
    app.register_blueprint(AddressRoutes.address, url_prefix='/api/address')
    # register payment routes
    app.register_blueprint(PaymentRoutes.payment, url_prefix='/api/payment')

    return app

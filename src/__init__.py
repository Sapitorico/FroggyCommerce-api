from flask import Flask
from flask_cors import CORS

from .routes import UserRoutes

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost"}})


def init_app(config):

    # Routes
    from .routes import AuthRoutes, ProductRoutes, UserRoutes

    # Configuration
    app.config.from_object(config)

    app.register_blueprint(AuthRoutes.auth, url_prefix='/api/auth')
    app.register_blueprint(UserRoutes.user, url_prefix='/api/users')
    app.register_blueprint(ProductRoutes.product, url_prefix='/api/products')

    return app

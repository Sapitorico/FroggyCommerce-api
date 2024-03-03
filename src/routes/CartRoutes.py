from flask import Blueprint, request

# Models
from src.models.ModelCart import ModelCart

# Security
from src.utils.Security import Security

# Rate limit
# from src.utils.decorators.Ratelimiter import rate_limit

cart = Blueprint('cart', __name__)


@cart.route('/', methods=['GET'])
@Security.verify_session
def get_cart(user_id):
    """
    Gets the users cart

    Args:
        user_id (str): user ID
    """
    if request.method == 'GET':
        response = ModelCart.get_cart(user_id)
        return response


@cart.route('/add', methods=['POST'])
@Security.verify_session
def add_to_cart(user_id):
    """
    Adds a product to the users cart

    Args:
        user_id (str): user ID
    """
    if request.method == 'POST':
        data = request.json
        valid_data = ModelCart.validate(data)
        if valid_data:
            return valid_data
        response = ModelCart.add_to_cart(user_id, data)
        return response


@cart.route('/remove/<string:id>', methods=['DELETE'])
@Security.verify_session
def delete(user_id, id):
    """
    Removes a product from the users cart

    Args:
        user_id (str): ID of the user.
        id (str): ID of the product to be removed from the cart
    """
    if request.method == 'DELETE':
        response = ModelCart.remove_to_cart(user_id, id)
        return response

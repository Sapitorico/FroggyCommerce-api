from flask import Blueprint, request

# Controller
from src.controllers.CartController import CartController

# Security
from src.utils.Security import Security

cart = Blueprint('cart', __name__)


@cart.route('/add', methods=['POST'])
@Security.verify_session
def add_to_cart(user_id):
    """
    Add an item to the user's cart.

    Args:
        user_id (str): The ID of the user.

    Returns:
        dict: The response containing the result of adding the item to the cart.
    """
    if request.method == 'POST':
        data = request.json
        response = CartController.add_to_cart(user_id, data)
        return response


@cart.route('/', methods=['GET'])
@Security.verify_session
def get_cart(user_id):
    """
    Retrieves the cart for the specified user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        dict: The response containing the cart information.
    """
    if request.method == 'GET':
        response = CartController.get_cart(user_id)
        return response


@cart.route('/remove/<string:id>', methods=['DELETE'])
@Security.verify_session
def remove(user_id, id):
    """
    Removes an item from the user's cart.

    Args:
        user_id (str): The ID of the user.
        id (str): The ID of the item to be removed.

    Returns:
        dict: The response containing the result of the removal operation.
    """
    if request.method == 'DELETE':
        response = CartController.remove_to_cart(user_id, id)
        return response


@cart.route('/empty', methods=['DELETE'])
@Security.verify_session
def empty_cart(user_id):
    """
    Empties the cart for the specified user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        dict: The response containing the status and message.
    """
    if request.method == 'DELETE':
        response = CartController.empty_cart(user_id)
        return response

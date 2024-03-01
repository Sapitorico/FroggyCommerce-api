from flask import Blueprint, request

# Entities
from src.models.entities.ShoppingCart import ShoppingCart

# Models
from src.models.ModelShoppingCart import ModelShoppingCart

# Security
from src.utils.Security import Security

cart = Blueprint('cart', __name__)


@cart.route('/', methods=['GET'])
@Security.verify_session
def get_cart(user_id):
    if request.method == 'GET':
        response = ModelShoppingCart.get_cart(user_id)
        return response


@cart.route('/add', methods=['POST'])
@Security.verify_session
def add_to_cart(user_id):
    if request.method == 'POST':
        data = request.json
        valid_data = ShoppingCart.validate(data)
        if valid_data:
            return valid_data
        response = ModelShoppingCart.add_to_cart(user_id, data)
        return response


@cart.route('/remove/<id>', methods=['DELETE'])
@Security.verify_session
def delete(user_id, id):
    if request.method == 'DELETE':
        response = ModelShoppingCart.remove_to_cart(user_id, id)
        return response

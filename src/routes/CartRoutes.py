from flask import Blueprint, request

# Entities
from src.models.entities.ShoppingCart import ShoppingCart

# Models
from src.models.ModelShoppingCart import ModelShoppingCart

# Security
from src.utils.Security import Security

cart = Blueprint('cart', __name__)

@cart.route('/', methods=['GET'])
def get_cart():
    access_result = Security.verify_session(request.headers)
    if isinstance(access_result, tuple):
        return access_result
    response = ModelShoppingCart.get_cart(access_result)
    return response
    


@cart.route('/add', methods=['POST'])
def add_to_cart():
    access_result = Security.verify_session(request.headers)
    if isinstance(access_result, tuple):
        return access_result
    if request.method == 'POST':
        data = request.json
        valid_data = ShoppingCart.validate(data)
        if valid_data:
            return valid_data
        response = ModelShoppingCart.add_to_cart(access_result, data)
        return response
    
@cart.route('/remove/<id>', methods=['DELETE'])
def delete(id):
    access_result = Security.verify_session(request.headers)
    if isinstance(access_result, tuple):
        return access_result
    response = ModelShoppingCart.remove_to_cart(access_result, id)
    return response
from flask import Blueprint, request

# Controllers
from src.controllers.ProductsController import ProductsController

# Security
from src.utils.Security import Security


product = Blueprint('product', __name__)


@product.route('/create', methods=['POST'])
@Security.verify_admin
def create_product():
    """
    Create a new product.

    This route is used to create a new product by sending a POST request with the required data.

    Returns:
        The response from the ProductsController.create_products method.
    """
    if request.method == 'POST':
        data = request.json
        response = ProductsController.create_products(data)
        return response


@product.route('/', methods=['GET'])
def get_products():
    """
    Retrieves all products.

    Returns:
        The response containing all products.
    """
    if request.method == 'GET':
        response = ProductsController.get_products()
        return response


@product.route('/<string:id>', methods=['GET'])
def get_product(id):
    """
    Get a product by its ID.

    Parameters:
    - id (str): The ID of the product.

    Returns:
    - response: The response containing the product information.
    """
    if request.method == 'GET':
        response = ProductsController.get_product_by_id(id)
        return response


@product.route('/update/<string:id>', methods=['PUT'])
@Security.verify_admin
def update_product(id):
    """
    Update a product with the given ID.

    Args:
        id (str): The ID of the product to update.

    Returns:
        dict: The response containing the result of the update operation.
    """
    if request.method == 'PUT':
        data = request.json
        response = ProductsController.update_product(id, data)
        return response


@product.route('/delete/<string:id>', methods=['DELETE'])
@Security.verify_admin
def delete_product(id):
    """
    Delete a product by its ID.

    Args:
        id (str): The ID of the product to be deleted.

    Returns:
        The response from the ProductsController.delete_product method.
    """
    if request.method == 'DELETE':
        response = ProductsController.delete_product(id)
        return response

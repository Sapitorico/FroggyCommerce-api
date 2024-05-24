from flask import Blueprint, request

# Controllers
from src.controllers.ProductsController import ProductsController

# Security
from src.services.SecurityService import SecurityService


product = Blueprint('product', __name__)


@product.route('/create', methods=['POST'])
@SecurityService.verify_admin
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
@SecurityService.verify_admin
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
@SecurityService.verify_admin
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


@product.route('/search', methods=['GET'])
@SecurityService.verify_admin
def search_product():
    """
    Search for a product by name.

    Returns:
        The response from the ProductsController.search method.
    """
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=12, type=int)
        name = request.args.get('name', type=str)
        response = ProductsController.search(page, per_page, name)
        return response


@product.route('/filter', methods=['GET'])
@SecurityService.verify_admin
def filter_product():
    """
    Filter products based on the specified category.

    Returns:
        The filtered products as a response.
    """
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=12, type=int)
        category = request.args.get('category', type=str)
        response = ProductsController.filter(page, per_page, category)
        return response


@product.route('/', methods=['GET'])
@SecurityService.verify_admin
def pagination_products():
    """
    Filter products based on the specified category.

    Returns:
        The filtered products as a response.
    """
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=12, type=int)
        response = ProductsController.pagination(page, per_page)
        return response

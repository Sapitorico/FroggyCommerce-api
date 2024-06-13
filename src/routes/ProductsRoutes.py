from flask import Blueprint, jsonify, request

# Controllers
from src.controllers.ProductsController import ProductsController

# Security
from src.services.SecurityService import SecurityService

# Utils
from src.utils.format_validations import validate


product = Blueprint('product', __name__)


@product.route('/', methods=['POST'])
@SecurityService.verify_admin
def create_product():
    """
    Create a new product.
    """
    if request.method == 'POST':
        data = request.json
        schema = {
            'name': {'type': 'string', 'minLength': 1, 'required': True},
            'description': {'type': 'string', 'minLength': 1, 'required': True},
            'price': {'type': 'number', 'minimum': 1, 'required': True},
            'stock': {'type': 'number', 'minimum': 1, 'required': True},
            'category': {'type': 'string', 'minLength': 1, 'required': True},
            'images': {
                'type': 'array',
                'required': True,
                'maxLength': 6,
                'items': {
                    'url': {'type': 'string', 'minLength': 1, 'required': True},
                    'is_main': {'type': 'boolean', 'valueRequired': True, 'maxRequired': 1, 'required': True}
                }
            }
        }
        error = validate(data, schema)
        if error:
            return jsonify({"success": False, "message": error}), 400
        response = ProductsController.create_products(data)
        if response == 'success':
            return jsonify({"success": True, "message": 'Product created successfully'}), 201
        if response == 'already_exits':
            return jsonify({"success": False, "message": 'Product already exists'}), 409
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@product.route('/<string:id>', methods=['GET'])
def get_product(id):
    """
    Get a product by its ID.
    """
    if request.method == 'GET':
        product, response = ProductsController.get_product_by_id(id)
        if response == 'success':
            return jsonify({"success": True, "message": "Product retrieved successfully",  "product": product}), 200
        if response == 'not_found':
            return jsonify({"success": False, "message": "Product not found"}), 404
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@product.route('/<string:id>', methods=['PUT'])
@SecurityService.verify_admin
def update_product(id):
    """
    Update a product with the given ID.
    """
    if request.method == 'PUT':
        data = request.json
        schema = {
            'name': {'type': 'string', 'minLength': 1, 'required': True},
            'description': {'type': 'string', 'minLength': 1, 'required': True},
            'price': {'type': 'number', 'minimum': 1, 'required': True},
            'stock': {'type': 'number', 'minimum': 1, 'required': True},
            'category': {'type': 'string', 'minLength': 1, 'required': True},
            'images': {
                'type': 'array',
                'required': True,
                'maxLength': 6,
                'items': {
                    'url': {'type': 'string', 'minLength': 1, 'required': True},
                    'is_main': {'type': 'boolean', 'valueRequired': True, 'maxRequired': 1, 'required': True}
                }
            }
        }
        error = validate(data, schema)
        if error:
            return jsonify({"success": False, "message": error}), 400
        response = ProductsController.update_product(id, data)
        if response == 'success':
            return jsonify({"success": True, "message": "Product updated successfully"}), 200
        if response == 'not_exists':
            return jsonify({"success": False, "message": "Product not found"}), 404
        if response == 'already_exists':
            return jsonify({"success": False, "message": "Product already exists"}), 409
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@product.route('/', methods=['GET'])
def pagination_products():
    """
    Filter products based on the specified category.
    """
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=12, type=int)
        category = request.args.get('category', type=str)
        name = request.args.get('name', type=str)
        products, total_pages, response = ProductsController.pagination(
            page, per_page, category, name)
        if response == 'success':
            return jsonify({"success": True, "message": "Products retrieved successfully", "products": products, "total_pages": total_pages}), 200
        if response == 'not_available':
            return jsonify({"success": False, "message": "Products not available"}), 200
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500

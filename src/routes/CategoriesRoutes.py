from flask import Blueprint, jsonify, request

# Controllers
from src.controllers.CategoriesController import CategoriesController

# Security
from src.services.SecurityService import SecurityService

# Utils
from src.utils.format_validations import validate

categories = Blueprint('categories', __name__)


@categories.route('/', methods=['GET'])
def get_categories():
    """
    Retrieves the categories.
    """
    if request.method == 'GET':
        categories, response = CategoriesController.get_categories()
        if response == 'success':
            return jsonify({"success": True, "message": "Categories retrieved successfully", "categories": categories}), 200
        if response == 'not_available':
            return jsonify({'success': False, 'message': 'Categories not available'}), 200
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@categories.route('/', methods=['POST'])
@SecurityService.verify_admin
def create_category():
    """
    Create the category.
    """
    if request.method == 'POST':
        data = request.json
        schema = {
            'name': {'type': 'string', 'minLength': 1, 'required': True},
            'image_url': {'type': 'string', 'minLength': 1, 'required': True}
        }
        error = validate(data, schema)
        if error:
            return jsonify({"success": False, "message": error}), 400
        response = CategoriesController.create_category(data)
        if response == 'success':
            return jsonify({"success": True, "message": 'Category created successfully'}), 201
        if response == 'already_exits':
            return jsonify({"success": False, "message": 'Category already exists'}), 409
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@categories.route('/<string:id>', methods=['PUT'])
@SecurityService.verify_admin
def update_category(id):
    """
    Update the category.
    """
    if request.method == 'PUT':
        data = request.json
        schema = {
            'name': {'type': 'string', 'minLength': 1, 'required': True},
            'image_url': {'type': 'string', 'minLength': 1, 'required': True}
        }
        error = validate(data, schema)
        if error:
            return jsonify({"success": False, "message": error}), 400
        response = CategoriesController.update_category(id, data)
        if response == 'success':
            return jsonify({"success": True, "message": 'Category updated successfully'}), 201
        if response == 'not_found':
            return jsonify({"success": False, "message": 'Category not found'}), 404
        if response == 'already_exits':
            return jsonify({"success": False, "message": 'Category already exists'}), 409
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500

from flask import Blueprint, jsonify, request

# Controller
from src.controllers.ReviewsController import ReviewsController

# Security
from src.services.SecurityService import SecurityService

# Utils
from src.utils.format_validations import validate


reviews = Blueprint('reviews', __name__)


@reviews.route('/', methods=['GET'])
@SecurityService.verify_session
def get_reviews(user_id):
    """
    Retrieves reviews and products without review for a given user.
    """
    if request.method == 'GET':
        reviews, products_without_review = ReviewsController.get_reviews(user_id)
        if reviews is not None or products_without_review is not None:
            return jsonify({
                'success': True,
                'message': 'Reviews retrieved successfully',
                'reviews': reviews,
                'products_without_review': products_without_review
            }), 200
        return jsonify({
            'success': False,
            'message': 'An unexpected error occurred'
        }), 500


@reviews.route('/<string:product_id>', methods=['POST'])
@SecurityService.verify_session
def create_review(user_id, product_id):
    """
    Create a review for a product.
    """
    if request.method == 'POST':
        data = request.json
        schema = {
            'rating': {'type': 'number', 'minimum': 1, 'maximum': 5, 'required': True},
            'review': {'type': 'string', 'minLength': 1, 'required': True},
        }
        error = validate(data, schema)
        if error is not None:
            return jsonify({'success': False, 'message': error}), 400
        response = ReviewsController.create_review(user_id, product_id, data)
        if response == 'not_purchased':
            return jsonify({'success': False, 'message': 'Product not purchased'}), 200
        if response == 'already_exists':
            return jsonify({'success': False, 'message': 'Review already exists'}), 200
        if response == 'success':
            return jsonify({'success': True, 'message': 'Review created successfully'}), 201
        return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@reviews.route('/<string:review_id>', methods=['GET'])
@SecurityService.verify_session
def get_review(user_id, review_id):
    """
    Retrieves a review based on the provided user ID and review ID.
    """
    if request.method == 'GET':
        response = ReviewsController.get_review(user_id, review_id)
        if response:
            return jsonify({
                'success': True,
                'message': 'Review retrieved successfully',
                'review': response
                }), 200
        return jsonify({'success': False, 'message': 'Review not found'}), 404


@reviews.route('/<string:review_id>', methods=['PUT'])
@SecurityService.verify_session
def update_review(user_id, review_id):
    """
    Update a review for a given user and review ID.
    """
    if request.method == 'PUT':
        schema = {
            'rating': {'type': 'number', 'minimum': 1, 'maximum': 5, 'required': True},
            'review': {'type': 'string', 'minLength': 1, 'required': True},
        }
        data = request.json
        error = validate(data, schema)
        if error is not None:
            return jsonify({'success': False, 'message': error}), 400
        response = ReviewsController.update_review(user_id, review_id, data)
        if response == 'not_exists':
            return jsonify({'success': False, 'message': 'Review not found'}), 404
        if response == 'success':
            return jsonify({'success': True, 'message': 'Review updated successfully'}), 200
        return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@reviews.route('/product/<string:product_id>', methods=['GET'])
def get_review_by_product(product_id):
    """
    Retrieve reviews for a specific product.
    """
    if request.method == 'GET':
        response = ReviewsController.get_reviews_by_product(product_id)
        if response is not None:
            return jsonify({'success': True, 'message': 'Reviews retrieved successfully', 'reviews': response}), 200
        return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500

from flask import Blueprint, request

# Controller
from src.controllers.ReviewsController import ReviewsController

# Security
from src.services.SecurityService import SecurityService

reviews = Blueprint('reviews', __name__)


@reviews.route('/', methods=['GET'])
@SecurityService.verify_session
def get_reviews(user_id):
    if request.method == 'GET':
        response = ReviewsController.get_reviews(user_id)
        return response


@reviews.route('/<string:product_id>', methods=['POST'])
@SecurityService.verify_session
def create_review(user_id, product_id):
    if request.method == 'POST':
        data = request.json
        response = ReviewsController.create_review(user_id, product_id, data)
        return response


@reviews.route('/<string:review_id>', methods=['GET'])
@SecurityService.verify_session
def get_review(user_id, review_id):
    if request.method == 'GET':
        response = ReviewsController.get_review(user_id, review_id)
        return response


@reviews.route('/<string:review_id>', methods=['PUT'])
@SecurityService.verify_session
def update_review(user_id, review_id):
    if request.method == 'PUT':
        data = request.json
        response = ReviewsController.update_review(user_id, review_id, data)
        return response


@reviews.route('/product/<string:product_id>', methods=['GET'])
def get_review_by_product(product_id):
    if request.method == 'GET':
        response = ReviewsController.get_reviews_by_product(product_id)
        return response

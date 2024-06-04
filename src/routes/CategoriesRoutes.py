from flask import Blueprint, request

# Controllers
from src.controllers.CategoriesController import CategoriesController

# Security
from src.services.SecurityService import SecurityService

categories = Blueprint('categories', __name__)


@categories.route('/', methods=['GET'])
@SecurityService.verify_admin
def get_categories():
    if request.method == 'GET':
        response = CategoriesController.get_categories()
        return response


@categories.route('/create', methods=['POST'])
@SecurityService.verify_admin
def create_category():
    if request.method == 'POST':
        data = request.json
        response = CategoriesController.create_category(data)
        return response


@categories.route('/update/<string:id>', methods=['PUT'])
@SecurityService.verify_admin
def update_category(id):
    if request.method == 'PUT':
        data = request.json
        response = CategoriesController.update_category(id, data)
        return response

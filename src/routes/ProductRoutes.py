from flask import Blueprint, request, jsonify

from src.models.entities.Products import Product

from src.models.ModelProduct import ModelProduct

from src.utils.Security import Security

product = Blueprint('product', __name__)


@product.route('/', methods=['GET'])
def get_products():
    if request.method == 'GET':
        response = ModelProduct.get_products()
        return response


@product.route('/<id>', methods=['GET'])
def get_product(id):
    if request.method == 'GET':
        response = ModelProduct.get_product_by_id(id)
        return response


@product.route('/create', methods=['POST'])
@Security.verify_admin
def create_product():
    if request.method == 'POST':
        data = request.json
        valid_data = Product.validate(data)
        if valid_data:
            return valid_data
        product = Product(name=data['name'],
                          description=data['description'],
                          price=data['price'],
                          stock=data['stock'],
                          category=data['category'])
        response = ModelProduct.create(product)
    return response


@product.route('/update/<id>', methods=['PUT'])
@Security.verify_admin
def update_product(id):
    if request.method == 'PUT':
        data = request.json
        valid_data = Product.validate(data)
        if valid_data:
            return valid_data
        response = ModelProduct.update_product(id, data)
        return response


@product.route('/delete/<id>', methods=['DELETE'])
@Security.verify_admin
def delete_product(id):
    if request.method == 'DELETE':
        response = ModelProduct.delete_product(id)
        return response

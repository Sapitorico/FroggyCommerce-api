from flask import Blueprint, request, jsonify

from src.models.entities.Products import Product

from src.models.ModelProduct import ModelProduct

from src.utils.Security import Security

product = Blueprint('product', __name__)


@product.route('/create', methods=['POST'])
def create_product():
    access_result = Security.verify_admin(request.headers)
    if access_result:
        return access_result
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

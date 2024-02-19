from flask import Blueprint, request, jsonify

from src.utils.Security import Security

product = Blueprint('product', __name__)

@product.route('/create', methods=['GET'])
def create_product():
    has_access = Security.verify_token(request.headers)
    if has_access:
        return has_access
    return jsonify({"message": "Token valido"}), 200
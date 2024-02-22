
from flask import jsonify


class Product():

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.price = kwargs.get('price')
        self.stock = kwargs.get('stock')
        self.category = kwargs.get('category')
        self.category_id = kwargs.get('category_id')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')

    @staticmethod
    def validate(product):
        if not product:
            return jsonify({"success": False, "message": "No se proporcionaron datos"}), 400
        if 'name' not in product:
            return jsonify({"success": False, "message": "Campo name requerido"}), 400
        if 'description' not in product:
            return jsonify({"success": False, "message": "Campo description requerido"}), 400
        if 'price' not in product:
            return jsonify({"success": False, "message": "Campop price requerido"}), 400
        if 'stock' not in product:
            return jsonify({"success": False, "message": "Campo stock requerido"}), 400
        if 'category' not in product:
            return jsonify({"success": False, "message": "Campo category requerido"}), 400
        return None

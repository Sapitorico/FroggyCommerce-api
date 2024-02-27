
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
            return jsonify({"success": False, "message": "Campo 'name' requerido"}), 400
        elif not isinstance(product['name'], str) or len(product['name']) == 0:
            return jsonify({"success": False, "message": "El campo 'name' debe ser una cadena no vacia"}), 400

        if 'description' not in product:
            return jsonify({"success": False, "message": "Campo 'description' requerido"}), 400
        elif not isinstance(product['description'], str) or len(product['description']) == 0:
            return jsonify({"success": False, "message": "El campo 'description' debe ser una cadena de caracteres"}), 400

        if 'price' not in product:
            return jsonify({"success": False, "message": "Campo 'price' requerido"}), 400
        elif not isinstance(product['price'], (int, float)) or isinstance(product['price'], bool) or product['price'] <= 0:
            return jsonify({"success": False, "message": "Campo 'price' debe ser un número y mayor que 0"}), 400

        if 'stock' not in product:
            return jsonify({"success": False, "message": "Campo stock requerido"}), 400
        elif not isinstance(product['stock'], int) or isinstance(product['stock'], bool) or product['stock'] <= 0:
            return jsonify({"success": False, "message": "Campo 'stock' debe ser un número y mayor que 0"}), 400

        if 'category' not in product:
            return jsonify({"success": False, "message": "Campo 'category' requerido"}), 400
        elif not isinstance(product['category'], str) or len(product['category']) == 0:
            return jsonify({"success": False, "message": "El campo 'category' debe ser una cadena no vacía"}), 400

        return None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

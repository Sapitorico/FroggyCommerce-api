

from flask import jsonify


class ShoppingCart:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.customer_id = kwargs.get('customer_id')
        self.product_id = kwargs.get('product_id')
        self.quantity = kwargs.get('quantity')

    @staticmethod
    def validate(data):
        if not data:
            return jsonify({"success": False, "message": "No se proporcionaron datos"}), 400

        if 'product_id' not in data:
            return jsonify({"success": False, "message": "Campo 'product_id' requerido"}), 400
        elif not isinstance(data['product_id'], str) or len(data['product_id']) == 0:
            return jsonify({"success": False, "message": "El campo 'product_id' debe ser una cadena no vacia"}), 400

        if 'quantity' not in data:
            return jsonify({"success": False, "message": "Campo 'quantity requerido"}), 400
        elif not isinstance(data['quantity'], int) or isinstance(data['quantity'], bool) or data['quantity'] <= 0:
            return jsonify({"success": False, "message": "Campo 'quantity' debe ser un número y mayor que 0"}), 400

        return None

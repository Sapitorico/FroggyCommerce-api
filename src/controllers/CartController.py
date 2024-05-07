from flask import jsonify

# Models
from src.models.CartModel import CartModel


class CartController():
    """
    Controller class for managing the user's shopping cart.
    """

    @classmethod
    def add_to_cart(cls, user_id, data):
        """
        Adds a product to the user's cart.

        Args:
            user_id (str): The ID of the user.
            data (dict): The data containing the product ID and quantity.

        Returns:
            tuple: A tuple containing the response JSON and status code.
        """
        validate = cls.validate(data)
        if validate:
            return validate
        cart = CartModel(None, user_id, data['product_id'], data['quantity'])
        response = cart.add()
        if not response:
            return jsonify({"success": False, "message": "Product not found"}), 404
        return jsonify({"success": True, "message": "Product successfully added to cart"}), 201

    @classmethod
    def get_cart(cls, user_id):
        """
        Retrieves the user's cart.

        Args:
            user_id (str): The ID of the user.

        Returns:
            tuple: A tuple containing the response JSON and status code.
        """
        cart = CartModel.get(user_id)
        if not cart:
            return jsonify({"success": False, "message": "Cart is empty"}), 404
        cart = [CartModel(id=item[0], name=item[1], price=float(item[2]),
                          quantity=item[3], total=item[4]).to_dict() for item in cart]
        return jsonify({"success": True, "message": "Cart retrieved successfully", "cart": cart}), 200

    @classmethod
    def remove_to_cart(cls, user_id, product_id):
        """
        Removes a product from the user's cart.

        Args:
            user_id (str): The ID of the user.
            product_id (str): The ID of the product to be removed.

        Returns:
            tuple: A tuple containing the response JSON and status code.
        """
        response = CartModel.remove(user_id, product_id)
        if not response:
            return jsonify({"success": False, "message": "Product is not in your cart"}), 404
        return jsonify({"success": True, "message": "Product successfully removed from cart"}), 200

    @classmethod
    def empty_cart(cls, user_id):
        """
        Empties the user's cart.

        Args:
            user_id (str): The ID of the user.

        Returns:
            tuple: A tuple containing the response JSON and status code.
        """
        response = CartModel.empty(user_id)
        if not response:
            return jsonify({"success": False, "message": "User not found"}), 404
        return jsonify({"success": True, "message": "Cart successfully emptied"}), 200

    @staticmethod
    def validate(data):
        """
        Validates the data for adding a product to the cart.

        Args:
            data (dict): The data containing the product ID and quantity.

        Returns:
            None or tuple: None if the data is valid, otherwise a tuple containing the response JSON and status code.
        """
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        if 'product_id' not in data:
            return jsonify({"success": False, "message": "'product_id' field is required"}), 400
        elif not isinstance(data['product_id'], str) or len(data['product_id']) == 0:
            return jsonify({"success": False, "message": "'product_id' field must be a non-empty string"}), 400

        if 'quantity' not in data:
            return jsonify({"success": False, "message": "'quantity' field is required"}), 400
        elif not isinstance(data['quantity'], int) or isinstance(data['quantity'], bool) or data['quantity'] <= 0:
            return jsonify({"success": False, "message": "'quantity' field must be a number and greater than 0"}), 400

        return None

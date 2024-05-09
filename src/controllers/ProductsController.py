from flask import jsonify

# Models
from src.models.ProductsModel import ProductsModel


class ProductsController():
    """
    Controller class for managing products in an e-commerce system.
    """

    @classmethod
    def create_products(cls, data):
        """
        Create a new product.

        Args:
            data (dict): A dictionary containing the product data.

        Returns:
            A JSON response indicating the success or failure of the operation.
        """
        validate = cls.validate(data)
        if validate:
            return validate
        product = ProductsModel(None, data['name'], data['description'], data['price'], data['stock'],
                                data['category'], None)
        response = product.create()
        if not response:
            return jsonify({"success": False, "message": 'Product already exists'}), 400
        return jsonify({"success": True, "message": 'Successfully created product'}), 201

    @classmethod
    def get_products(cls):
        """
        Get all products.

        Returns:
            A JSON response containing the list of products.
        """
        products = ProductsModel.get_all()
        if not products:
            return jsonify({"success": False, "message": "No products found"}), 404
        products = [ProductsModel(product[0], product[1], product[2], product[3], product[4],
                                  product[5], None, product[6], product[7]).to_dict() for product in products]
        return jsonify({"success": True, "message": "Products retrieved successfully", "products": products}), 200

    @classmethod
    def get_product_by_id(cls, id):
        """
        Get a product by its ID.

        Args:
            id (str): The ID of the product.

        Returns:
            A JSON response containing the product information.
        """
        product = ProductsModel.get_by_id(id)
        if not product:
            return jsonify({"success": False, "message": "Product not found"}), 404
        product = ProductsModel(product[0], product[1], product[2], product[3], product[4],
                                product[5], None, product[6], product[7]).to_dict()
        return jsonify({"success": True, "message": "Product retrieved successfully",  "product": product}), 200

    @classmethod
    def update_product(cls, id, data):
        """
        Update a product.

        Args:
            id (str): The ID of the product.
            data (dict): A dictionary containing the updated product data.

        Returns:
            A JSON response indicating the success or failure of the operation.
        """
        validate = cls.validate(data)
        if validate:
            return validate
        product = ProductsModel(id, data['name'], data['description'], data['price'],
                                data['stock'], data['category'], None)
        response = product.update()
        if not response:
            return jsonify({"success": False, "message": "Product not found"}), 404
        return jsonify({"success": True, "message": "Product successfully upgraded"}), 200

    @classmethod
    def delete_product(cls, id):
        """
        Delete a product.

        Args:
            id (str): The ID of the product.

        Returns:
            A JSON response indicating the success or failure of the operation.
        """
        response = ProductsModel.delete(id)
        if not response:
            return jsonify({"success": False, "message": "Product not found"}), 404
        return jsonify({"success": True, "message": "Product successfully deleted"}), 200

    @staticmethod
    def validate(product):
        """
        Validate the product data.

        Args:
            product (dict): A dictionary containing the product data.

        Returns:
            None if the data is valid, otherwise a JSON response indicating the validation error.
        """
        if not product:
            return jsonify({"success": False, "message": "No data provided"}), 400

        if 'name' not in product:
            return jsonify({"success": False, "message": "'name' field is required"}), 400
        elif not isinstance(product['name'], str) or len(product['name']) == 0:
            return jsonify({"success": False, "message": "'name' field must be a non-empty string"}), 400

        if 'description' not in product:
            return jsonify({"success": False, "message": "'description' field is required"}), 400
        elif not isinstance(product['description'], str) or len(product['description']) == 0:
            return jsonify({"success": False, "message": "'description' field must be a string of characters"}), 400

        if 'price' not in product:
            return jsonify({"success": False, "message": "'price' field is required"}), 400
        elif not isinstance(product['price'], (int, float)) or isinstance(product['price'], bool) or product['price'] <= 0:
            return jsonify({"success": False, "message": "'price' field must be a number and greater than 0"}), 400

        if 'stock' not in product:
            return jsonify({"success": False, "message": "'stock' field is required"}), 400
        elif not isinstance(product['stock'], int) or isinstance(product['stock'], bool) or product['stock'] <= 0:
            return jsonify({"success": False, "message": "'stock' field must be a number and greater than 0"}), 400

        if 'category' not in product:
            return jsonify({"success": False, "message": "'category' field is required"}), 400
        elif not isinstance(product['category'], str) or len(product['category']) == 0:
            return jsonify({"success": False, "message": "'category' field must be a non-empty string"}), 400

        return None

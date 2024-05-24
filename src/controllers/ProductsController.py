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
        product = ProductsModel(None, name=data['name'], description=data['description'], price=data['price'], stock=data['stock'],
                                category=data['category'], images=data['images'])
        response = product.create()
        if not response:
            return jsonify({"success": False, "message": 'Product already exists'}), 400
        return jsonify({"success": True, "message": 'Successfully created product'}), 201

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
        product = ProductsModel(id=product[0], name=product[1], description=product[2], price=product[3], stock=product[4],
                                category=product[5], created_at=product[6], updated_at=product[7], images=product[8]).to_dict()
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
        product = ProductsModel(id=id, name=data['name'], description=data['description'], price=data['price'],
                                stock=data['stock'], category=data['category'], images=data['images'])
        response = product.update()
        if not response:
            return jsonify({"success": False, "message": "Product not found"}), 404
        if response == 'already_exists':
            return jsonify({"success": False, "message": "Product already exists"}), 400
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

    @classmethod
    def search(cls, page, per_page, name):
        """
        Search for products by name.

        Args:
            name (str): The name of the product to search for.

        Returns:
            A JSON response containing the search results.

        Raises:
            400 Bad Request: If no search query is provided.
            404 Not Found: If no products are found.

        """
        if not page or not per_page or not name:
            return jsonify({"success": False, "message": "No page or per_page or search query provided"}), 400
        products, total_pages = ProductsModel.search_by_name(
            page, per_page, name)
        if not products:
            return jsonify({"success": False, "message": "No products found"}), 404
        products = [ProductsModel(id=product[0], name=product[1], description=product[2], category=product[3], price=product[4],
                                  stock=product[5], created_at=product[6], updated_at=product[7], images=product[8]).to_dict() for product in products]
        return jsonify({"success": True, "message": "Products retrieved successfully", "products": products, "total_pages": total_pages}), 200

    @classmethod
    def filter(cls, page, per_page, category):
        """
        Filter products by category.

        Args:
            category (str): The category to filter by.

        Returns:
            Flask Response: A JSON response containing the filtered products.

        Raises:
            HTTPException: If no category query is provided or no products are found.

        """
        if not page or not per_page or not category:
            return jsonify({"success": False, "message": "No page or per_page or category query provided"}), 400
        products, total_pages = ProductsModel.filter_by_category(
            page, per_page, category)
        if not products:
            return jsonify({"success": False, "message": "No products found"}), 404
        products = [ProductsModel(id=product[0], name=product[1], description=product[2], category=product[3], price=product[4],
                                  stock=product[5], created_at=product[6], updated_at=product[7], images=product[8]).to_dict() for product in products]
        return jsonify({"success": True, "message": "Products retrieved successfully", "products": products, "total_pages": total_pages}), 200

    @classmethod
    def pagination(cls, page, per_page):
        if not page or not per_page:
            return jsonify({"success": False, "message": "No page or per_page query provided"}), 400
        products, total_pages = ProductsModel.pagination(page, per_page)
        if not products:
            return jsonify({"success": False, "message": "No products found"}), 404
        products = [ProductsModel(id=product[0], name=product[1], description=product[2], category=product[3], price=product[4],
                                  stock=product[5], created_at=product[6], updated_at=product[7]).to_dict() for product in products]
        return jsonify({"success": True, "message": "Products retrieved successfully", "products": products, "total_pages": total_pages}), 200

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

        if 'images' not in product:
            return jsonify({"success": False, "message": "'images' field is required"}), 400
        elif not isinstance(product['images'], list) or len(product['images']) == 0 or len(product['images']) > 6:
            return jsonify({"success": False, "message": "'images' field must be a non-empty array and cannot have more than 6 images"}), 400
        else:
            for image in product['images']:
                if not isinstance(image, dict) or 'url' not in image or 'is_main' not in image or not isinstance(image['url'], str) or not isinstance(image['is_main'], bool):
                    return jsonify({"success": False, "message": "Each item in 'images' must be a dictionary with 'url' (string) and 'is_main' (true or false) keys"}), 400
            main_images = [image for image in product['images']
                           if image['is_main'] == True]
            if len(main_images) != 1:
                return jsonify({"success": False, "message": "Exactly one image should have 'is_main' set to True"}), 400
        return None

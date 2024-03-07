import uuid
from datetime import datetime
from flask import jsonify

# Entities
from src.models.entities.Products import Product


class ModelProduct():

    @classmethod
    def create(cls, db, product):
        """
        Create a new product in the database.

        Args:
            product (Product): Object representing the product to create.
        """
        try:
            cursor = db.cursor()
            product_id = str(uuid.uuid4())
            category_id = str(uuid.uuid4())
            cursor.callproc("Create_product", (product_id,
                                               product.name,
                                               product.description,
                                               product.price,
                                               product.stock,
                                               category_id,
                                               product.category))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'already exist':
                return jsonify({"success": False, "message": 'Product already exists'}), 400
            elif message == 'success':
                db.commit()
                return jsonify({"success": True, "message": 'Successfully created product'}), 201
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def get_products(cls, db):
        """
        Get all products stored in the database.
        """
        try:
            cursor = db.cursor()
            cursor.callproc("Products_list")
            for result in cursor.stored_results():
                products = result.fetchall()
            products = [Product(id=product[0],
                                name=product[1],
                                description=product[2],
                                price=product[3],
                                stock=product[4],
                                category=product[5],
                                created_at=product[6],
                                updated_at=product[7]).to_dict() for product in products]
            return jsonify({"success": True, "message": "Products retrieved successfully", "products": products}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def get_product_by_id(cls, db, id):
        """
        Get a product from the database by its ID.

        Args:
            id (str): ID of the product.
        """
        try:
            cursor = db.cursor()
            cursor.callproc("Product_by_id", (id,))
            for result in cursor.stored_results():
                product = result.fetchone()
            if not product:
                return jsonify({"success": False, "message": "Product not found"}), 404
            product = Product(id=product[0],
                              name=product[1],
                              description=product[2],
                              price=product[3],
                              stock=product[4],
                              category=product[5],
                              created_at=product[6],
                              updated_at=product[7]).to_dict()
            return jsonify({"success": True, "message": "Product retrieved successfully",  "product": product}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def update_product(cls, db, id, product):
        """
        Update an existing product in the database.

        Args:
            id (str): ID of the product to update.
            product (dict): Updated product data.
        """
        try:
            cursor = db.cursor()
            category_id = str(uuid.uuid4())
            cursor.callproc("Update_product", (id,
                                               product['name'],
                                               product['description'],
                                               product['price'],
                                               product['stock'],
                                               category_id,
                                               product['category']))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                return jsonify({"success": False, "message": "Product not found"}), 404
            elif message == 'success':
                db.commit()
                return jsonify({"success": True, "message": "Product successfully upgraded"}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def delete_product(cls, db, id):
        """
        Delete an existing product from the database.

        Args:
            id (str): ID of the product to delete.
        """
        try:
            cursor = db.cursor()
            cursor.callproc("Delete_product", (id,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                return jsonify({"success": False, "message": "Product not found"}), 404
            elif message == 'success':
                db.commit()
                return jsonify({"success": True, "message": "Product successfully deleted"}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            cursor.close()

    @staticmethod
    def validate(product):
        """
        Delete an existing product from the database.

        Args:
            id (str): ID of the product to delete.
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

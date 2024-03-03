
from uuid import uuid4
from flask import jsonify

# Database connection
from src.database.db_conection import DBConnection

db = DBConnection()


class ModelCart():

    @classmethod
    def get_cart(cls, user_id):
        """
        Get the user's shopping cart.

        Args:
            user_id (str): ID of the user whose cart is to be fetched.
        """
        try:
            cursor = db.connection.cursor()
            cursor.callproc("Get_cart", (user_id,))
            for results in cursor.stored_results():
                result = results.fetchall()

            cart = []
            for item in result:
                cart.append({
                    "id": item[0],
                    "name": item[1],
                    "price": item[2],
                    "quantity": item[3],
                    "total": item[4]
                })

            return jsonify({"success": True, "cart": cart}), 200
        except Exception as e:
            return jsonify({"success": True, "error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def add_to_cart(cls, user_id, data):
        """
        Add a product to the user's shopping cart.

        Args:
            user_id (str): ID of the user to whom the product will be added.
            data (dict): Product data to be added, including 'product_id' and 'quantity'.

        """
        try:
            cursor = db.connection.cursor()
            cart_id = str(uuid4())
            cursor.callproc(
                "Add_to_cart", (data['product_id'], user_id, data['quantity'], cart_id))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                return jsonify({"success": False, "message": "Product not found"}), 404
            elif message == 'success':
                db.connection.commit()
                return jsonify({"success": True, "message": "Product successfully added to cart"}), 201
        except Exception as e:
            return jsonify({"success": True, "error": str(e)})
        finally:
            cursor.close()

    @classmethod
    def remove_to_cart(cls, user_id, product_id):
        """
        Remove a product from the user's shopping cart.

        Args:
            user_id (str): ID of the user from whom the product will be removed from the cart.
            product_id (str): ID of the product to be removed from the cart.
        """
        try:
            cursor = db.connection.cursor()
            cursor.callproc("Remove_to_cart", (user_id, product_id))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                return jsonify({"success": False, "message": "Product is not in your cart"}), 404
            elif message == 'success':
                db.connection.commit()
                return jsonify({"success": True, "message": "Product successfully removed from cart"}), 200
        except Exception as e:
            return jsonify({"success": True, "error": str(e)})
        finally:
            cursor.close()

    @staticmethod
    def validate(data):
        """
        Validate the provided data for adding a product to the cart.

        Args:
            data (dict): Product data to validate.
        """
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

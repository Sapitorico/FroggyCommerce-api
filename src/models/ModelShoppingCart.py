
# Database
from uuid import uuid4

from flask import jsonify
from src.database.db_conection import connect_to_mysql

db = connect_to_mysql()


class ModelShoppingCart():

    @classmethod
    def get_cart(cls, user_id):
        try:
            cursor = db.cursor()
            sql = "SELECT shopping_cart.product_id, products.name, products.price, shopping_cart.quantity, (products.price * shopping_cart.quantity) AS total FROM shopping_cart INNER JOIN products ON shopping_cart.product_id = products.id WHERE shopping_cart.customer_id = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()

            if not result:
                return jsonify({"success": False, "message": "No hay productos en el carrito"}), 404

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
            raise Exception(f"Error: {str(e)}")

        finally:
            cursor.close()

    @classmethod
    def add_to_cart(cls, user_id, data):
        try:
            cursor = db.cursor()

            product_id = data['product_id']
            cursor.execute(
                "SELECT id FROM products WHERE id = %s", (product_id,))
            product_exists = cursor.fetchone()

            if not product_exists:
                return jsonify({"success": False, "message": "El producto no existe"}), 404

            sql = "SELECT id FROM shopping_cart WHERE customer_id = %s AND product_id = %s"
            cursor.execute(sql, (user_id, product_id,))
            result = cursor.fetchone()

            if result:
                sql = "UPDATE shopping_cart SET quantity = %s WHERE id = %s"
                cursor.execute(sql, (data['quantity'], result[0]))
                db.commit()
                return jsonify({"success": True, "message": "Producto agregado al carrito con éxito"}), 201

            sql = "INSERT INTO shopping_cart (id, customer_id, product_id, quantity) VALUES (%s, %s, %s, %s)"
            cart_id = str(uuid4())
            cursor.execute(
                sql, (cart_id, user_id, product_id, data['quantity']))
            db.commit()
            return jsonify({"success": True, "message": "Producto agregado al carrito con éxito"}), 201

        except Exception as e:
            raise Exception(f"Error: {str(e)}")

        finally:
            cursor.close()

    @classmethod
    def remove_to_cart(cls, user_id, product_id):
        try:
            cursor = db.cursor()

            sql = "SELECT id FROM shopping_cart WHERE customer_id = %s AND product_id = %s"
            cursor.execute(sql, (user_id, product_id))
            result = cursor.fetchone()

            if not result:
                return jsonify({"success": False, "message": "El producto no está en el carrito"}), 404

            sql = "DELETE FROM shopping_cart WHERE customer_id = %s AND product_id = %s"
            cursor.execute(sql, (user_id, product_id))
            db.commit()
            return jsonify({"success": True, "message": "Producto eliminado del carrito con éxito"}), 200

        except Exception as e:
            raise Exception(f"Error: {str(e)}")

        finally:
            cursor.close()

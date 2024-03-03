import uuid
from datetime import datetime
from flask import jsonify

# Database connection
from src.database.db_conection import DBConnection

# Entities
from src.models.entities.Products import Product

db = DBConnection()


class ModelProduct():

    @classmethod
    def create(cls, product):
        try:
            cursor = db.connection.cursor()
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
                db.connection.commit()
                return jsonify({"success": True, "message": 'Successfully created product'}), 201
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
        finally:
            cursor.close()

    @classmethod
    def get_products(cls):
        try:
            cursor = db.connection.cursor()
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
            return jsonify({"success": True, "Products": [products]}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
        finally:
            cursor.close()

    @classmethod
    def get_product_by_id(cls, id):
        try:
            cursor = db.connection.cursor()
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
            return jsonify({"success": True, "Product": product}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
        finally:
            cursor.close()

    @classmethod
    def update_product(cls, id, product):
        try:
            cursor = db.connection.cursor()
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
                db.connection.commit()
                return jsonify({"success": True, "message": "Product successfully upgraded"}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
        finally:
            cursor.close()

    @classmethod
    def delete_product(cls, id):
        try:
            cursor = db.connection.cursor()
            # sql = "SELECT id FROM products WHERE id = %s"
            # cursor.execute(sql, (id,))
            # existing_product = cursor.fetchone()
            # if not existing_product:
            #     return jsonify({"success": False, "message": "Producto no encontrado"}), 404
            # sql = "DELETE FROM products WHERE id = %s"
            cursor.callproc("Delete_product", (id,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                return jsonify({"success": False, "message": "Product not found"}), 404
            elif message == 'success':
                db.connection.commit()
                return jsonify({"success": True, "message": "Product successfully removed"}), 200
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
        finally:
            cursor.close()

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

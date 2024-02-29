import uuid
from datetime import datetime
from flask import jsonify

from src.database.db_conection import DBConnection

# Entities
from src.models.entities.Products import Product

db = DBConnection()


class ModelProduct():

    @classmethod
    def create(cls, product):
        try:
            cursor = db.connection.cursor()

            sql = "SELECT id FROM products WHERE name = %s"
            cursor.execute(sql, (product.name,))
            existing_product = cursor.fetchall()

            if existing_product:
                return jsonify({"success": False, "message": 'El producto ya existe'}), 400

            sql = "SELECT id FROM categories WHERE name = %s"
            cursor.execute(sql, (product.category,))
            category_row = cursor.fetchone()

            if category_row:
                category_id = category_row[0]
            else:
                category_id = str(uuid.uuid4())
                sql = """ INSERT INTO categories (id, name) VALUES (%s, %s) """
                cursor.execute(sql, (category_id, product.category,))

            sql = """ INSERT INTO products (id,
                                            name,
                                            description,
                                            price,
                                            stock,
                                            category_id,
                                            created_at,
                                            updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
            product_id = str(uuid.uuid4())
            cursor.execute(sql, (product_id,
                                 product.name,
                                 product.description,
                                 product.price,
                                 product.stock,
                                 category_id,
                                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            db.connection.commit()
            return jsonify({"success": True, "message": 'Producto creado con éxito'}), 201
        except Exception as e:
            raise Exception(
                f"Error al conectar con la base de datos: {str(e)}")
        finally:
            cursor.close()

    @classmethod
    def get_products(cls):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT p.id, p.name, p.description, p.price, p.stock, c.name as category, p.created_at, p.updated_at
                FROM products p
                INNER JOIN categories c ON p.category_id = c.id
            """
            cursor.execute(sql)
            products = cursor.fetchall()
            products = [Product(id=product[0],
                                name=product[1],
                                description=product[2],
                                price=product[3],
                                stock=product[4],
                                category=product[5],
                                created_at=product[6],
                                updated_at=product[7]) for product in products]
            return jsonify({"success": True, "Products": [product.to_dict() for product in products]}), 200
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
        finally:
            cursor.close()

    @classmethod
    def get_product_by_id(cls, id):
        try:
            cursor = db.connection.cursor()
            sql = """
                SELECT p.id, p.name, p.description, p.price, p.stock, c.name as category, p.created_at, p.updated_at
                FROM products p
                INNER JOIN categories c ON p.category_id = c.id
                WHERE p.id = %s
            """
            cursor.execute(sql, (id,))
            product = cursor.fetchone()
            if not product:
                return jsonify({"success": False, "message": "Producto no encontrado"}), 404
            product = Product(id=product[0],
                              name=product[1],
                              description=product[2],
                              price=product[3],
                              stock=product[4],
                              category=product[5],
                              created_at=product[6],
                              updated_at=product[7])
            return jsonify({"success": True, "Product": product.to_dict()}), 200
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
        finally:
            cursor.close()

    @classmethod
    def update_product(cls, id, product):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id FROM products WHERE id = %s"
            cursor.execute(sql, (id,))
            existing_product = cursor.fetchone()
            if not existing_product:
                return jsonify({"success": False, "message": "Producto no encontrado"}), 404

            sql = "SELECT id FROM categories WHERE name = %s"
            cursor.execute(sql, (product['category'],))
            category_row = cursor.fetchone()

            if category_row:
                category_id = category_row[0]
            else:
                category_id = str(uuid.uuid4())
                sql = """ INSERT INTO categories (id, name) VALUES (%s, %s) """
                cursor.execute(sql, (category_id, product['category'],))
            sql = """
                UPDATE products
                SET name = %s,
                    description = %s,
                    price = %s,
                    stock = %s,
                    category_id = %s,
                    updated_at = %s
                WHERE id = %s
            """
            cursor.execute(sql, (product['name'],
                                 product['description'],
                                 product['price'],
                                 product['stock'],
                                 category_id,
                                 datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                 id))
            db.connection.commit()
            return jsonify({"success": True, "message": "Producto actualizado con éxito"}), 200
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
        finally:
            cursor.close()

    @classmethod
    def delete_product(cls, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id FROM products WHERE id = %s"
            cursor.execute(sql, (id,))
            existing_product = cursor.fetchone()
            if not existing_product:
                return jsonify({"success": False, "message": "Producto no encontrado"}), 404
            sql = "DELETE FROM products WHERE id = %s"
            cursor.execute(sql, (id,))
            db.connection.commit()
            return jsonify({"success": True, "message": "Producto eliminado con éxito"}), 200
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
        finally:
            cursor.close()

import uuid
from datetime import datetime
from flask import jsonify

from src.database.db_conection import connect_to_mysql

db = connect_to_mysql()


class ModelProduct():

    @classmethod
    def create(cls, product):
        try:
            cursor = db.cursor()
            sql = """ INSERT INTO categories (id, name) VALUES (%s, %s) """
            category_id = str(uuid.uuid4())
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
                                 datetime.now().strftime('%Y-%m-%d %H:%M:%S')),)
            db.commit()
            cursor.close()
            return jsonify({"success": True, "message": 'Prodcuto creado con éxito'}), 201
        except Exception as e:
            raise Exception(f"Error: {str(e)}")

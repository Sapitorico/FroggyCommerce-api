import uuid

from flask import json

# Database service
from src.services.DataBaseService import DataBaseService

# Utils
from src.utils.format_datetime import format_datetime

conn = DataBaseService()


class ProductsModel():
    """
    Represents a product in the e-commerce system.

    Attributes:
        id (str): The unique identifier of the product.
        name (str): The name of the product.
        description (str): The description of the product.
        price (float): The price of the product.
        stock (int): The stock quantity of the product.
        category (str): The category of the product.
        images (dic): The product images url's
        category_id (str): The unique identifier of the category.
        created_at (datetime): The timestamp when the product was created.
        updated_at (datetime): The timestamp when the product was last updated.
    """

    def __init__(self, id=None, name=None, description=None, price=None, stock=None, category=None,
                 images=None, category_id=None, created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category = category
        self.images = images
        self.category_id = category_id
        self.created_at = created_at
        self.updated_at = updated_at

    def create(self):
        """
        Creates a new product in the database.
        """
        try:
            cursor = conn.get_cursor()

            sql = "SELECT id FROM products WHERE name = %s;"
            cursor.execute(sql, (self.name,))
            result = cursor.fetchone()

            if result:
                return 'already_exits'

            sql = "SELECT id FROM categories WHERE name = %s;"
            cursor.execute(sql, (self.category,))
            result = cursor.fetchone()

            if result:
                category_id = result[0]
            else:
                category_id = str(uuid.uuid4())
                sql = "INSERT INTO categories (id, name) VALUES (%s, %s);"
                cursor.execute(sql, (category_id, self.category))

            sql = """
            INSERT INTO products (
                id,
                name,
                description,
                price,
                stock,
                category_id
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            );
            """
            product_id = str(uuid.uuid4())
            cursor.execute(sql, (product_id, self.name,
                           self.description, self.price, self.stock, category_id,))

            for image in self.images:
                image_id = str(uuid.uuid4())
                image_url = image['url']
                is_main = 1 if image['is_main'] else 0
                sql = """
                INSERT INTO products_images (
                    id,
                    product_id,
                    image_url,
                    is_main
                ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s
                );
                """
                cursor.execute(
                    sql, (image_id, product_id, image_url, is_main,))
            conn.connection.commit()
            return 'success'
        except Exception as e:
            conn.connection.rollback()
            print(f"An error occurred: {e}")
            return 'failure'
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, id):
        """
        Retrieves a product by its ID from the database.
        """
        try:
            cursor = conn.get_cursor()

            sql = """
            SELECT 
                p.id,
                p.name,
                p.description,
                p.price,
                p.stock,
                c.name AS category,
                p.created_at,
                p.updated_at,
                JSON_ARRAYAGG(JSON_OBJECT('image_url',
                                i.image_url,
                                'is_main',
                                i.is_main)) AS images
            FROM
                products p
                    INNER JOIN
                categories c ON p.category_id = c.id
                    LEFT JOIN
                products_images i ON i.product_id = %s
            WHERE
                p.id = %s
            GROUP BY p.id , p.name , p.description , p.price , p.stock , c.name , p.created_at , p.updated_at;
            """
            cursor.execute(sql, (id, id,))
            product = cursor.fetchone()

            if product:
                return product, 'success'
            return None, 'not_found'
        except Exception as e:
            print(f'An error occurred: {e}')
            return None, 'failure'
        finally:
            conn.close()

    def update(self):
        """
        Updates the product in the database.
        """
        try:
            cursor = conn.get_cursor()

            sql = "SELECT id FROM products WHERE id = %s;"
            cursor.execute(sql, (self.id,))
            result = cursor.fetchone()
            
            if not result:
                return 'not_exists'

            sql = "SELECT id FROM products WHERE name = %s AND id != %s;"
            cursor.execute(sql, (self.name, self.id,))
            result = cursor.fetchone()
            
            if result:
                return 'already_exists'

            sql = "SELECT id FROM categories WHERE name = %s;"
            cursor.execute(sql, (self.category,))
            result = cursor.fetchone()
            
            if result:
                category_id = result[0]
            else:
                category_id = str(uuid.uuid4())
                sql = "INSERT INTO categories (id, name) VALUES (%s, %s);"
                cursor.execute(sql, (category_id, self.category))

            sql = """
            UPDATE products 
            SET 
                name = %s,
                description = %s,
                price = %s,
                stock = %s,
                category_id = %s
            WHERE
                id = %s;
            """
            cursor.execute(sql, (self.name, self.description,
                           self.price, self.stock, category_id, self.id,))

            sql = "DELETE FROM products_images WHERE product_id = %s;"
            cursor.execute(sql, (self.id,))

            for image in self.images:
                image_id = str(uuid.uuid4())
                image_url = image['url']
                is_main = 1 if image['is_main'] else 0
                sql = """
                INSERT INTO products_images (
                    id,
                    product_id,
                    image_url,
                    is_main
                ) VALUES (
                    %s,
                    %s,
                    %s,
                    %s
                );
                """
                cursor.execute(sql, (image_id, self.id, image_url, is_main,))
            conn.connection.commit()
            return 'success'
        except Exception as e:
            conn.connection.rollback()
            print(f'An error occurred: {e}')
            return 'failure'
        finally:
            conn.close()

    @classmethod
    def pagination(cls, page, per_page, category=None, name=None):
        """
        Perform pagination on the products table based on the given parameters.
        """
        try:
            cursor = conn.get_cursor()

            sql = """
            SELECT
                CEIL(COUNT(*) / %s)
            FROM
                products p
                INNER JOIN categories c ON p.category_id = c.id
            WHERE
                (%s IS NULL OR c.name LIKE %s)
                AND (%s IS NULL OR p.name LIKE CONCAT('%%', %s, '%%'))
            """
            cursor.execute(sql, (per_page, category, category, name, name))
            total_pages = cursor.fetchone()[0]

            offset = (page - 1) * per_page

            sql = """
            SELECT
                p.id,
                p.name,
                p.description,
                c.name as category,
                p.price,
                p.stock,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'image_url', i.image_url,
                        'is_main', i.is_main
                    )
                ) as images,
                p.created_at,
                p.updated_at
            FROM
                products p
            INNER JOIN
                categories c ON p.category_id = c.id
            LEFT JOIN
                products_images i ON p.id = i.product_id
            WHERE
                (%s IS NULL OR c.name LIKE %s)
                AND (%s IS NULL OR p.name LIKE CONCAT('%%', %s, '%%'))
            GROUP BY 
                p.id, 
                p.name, 
                p.description, 
                p.price, 
                p.stock, 
                c.name, 
                p.created_at, 
                p.updated_at
            ORDER BY 
                p.created_at DESC
            LIMIT %s
            OFFSET %s;
            """
            cursor.execute(
                sql, (category, category, name, name, per_page, offset))
            products = cursor.fetchall()

            if products:
                return products, total_pages, 'success'
            return None, total_pages, 'not_available'
        except Exception as e:
            print(f'An error occurred: {e}')
            return None, None, 'failure'
        finally:
            conn.close()

    def to_dict(self):
        """
        Converts the product object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "images": json.loads(self.images) if self.images else [],
            "created_at": format_datetime(self.created_at),
            "updated_at": format_datetime(self.updated_at)
        }

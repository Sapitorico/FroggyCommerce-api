import uuid

# Database service
from src.services.DataBaseService import DataBaseService

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
        category_id (str): The unique identifier of the category.
        created_at (datetime, optional): The timestamp when the product was created.
        updated_at (datetime, optional): The timestamp when the product was last updated.
    """

    def __init__(self, id, name, description, price, stock, category, category_id=None, created_at=None, updated_at=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.category = category
        self.category_id = category_id if category_id is not None else str(
            uuid.uuid4())
        self.created_at = created_at
        self.updated_at = updated_at

    def create(self):
        """
        Creates a new product in the database.

        Returns:
            bool: True if the product was successfully created, False otherwise.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Create_product", (self.id, self.name, self.description, self.price,
                                               self.stock, self.category_id, self.category))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'success':
                conn.connection.commit()
                return True
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        """
        Retrieves all products from the database.

        Returns:
            list: A list of dictionaries representing the products.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Products_list")
            for result in cursor.stored_results():
                products = result.fetchall()
            if products:
                return products
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, id):
        """
        Retrieves a product by its ID from the database.

        Args:
            id (str): The ID of the product to retrieve.

        Returns:
            dict: A dictionary representing the product, or None if not found.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Product_by_id", (id,))
            for result in cursor.stored_results():
                product = result.fetchone()
            if product:
                return product
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def update(self):
        """
        Updates the product in the database.

        Returns:
            bool: True if the product was successfully updated, False otherwise.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Update_product", (self.id, self.name, self.description, self.price,
                                               self.stock, self.category_id, self.category))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'success':
                conn.connection.commit()
                return True
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    @classmethod
    def delete(cls, id):
        """
        Deletes the product from the database.

        Args:
            id (str): The ID of the product to delete.

        Returns:
            bool: True if the product was successfully deleted, False otherwise.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Delete_product", (id,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'success':
                conn.connection.commit()
                return True
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def search_by_name(cls, name):
        """
        Search products by name.

        Args:
            name (str): The name of the product to search for.

        Returns:
            list: A list of products matching the given name.

        Raises:
            Exception: If an error occurs during the search.

        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Search_products", (name,))
            for result in cursor.stored_results():
                products = result.fetchall()
            if products:
                return products
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def filter_by_category(cls, category):
        """
        Filter products by category.

        Args:
            category (str): The category to filter by.

        Returns:
            list: A list of products matching the specified category.

        Raises:
            Exception: If an error occurs while filtering the products.

        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Filter_by_category", (category,))
            for result in cursor.stored_results():
                products = result.fetchall()
            if products:
                return products
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def to_dict(self):
        """
        Converts the product object to a dictionary.

        Returns:
            dict: A dictionary representation of the product.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

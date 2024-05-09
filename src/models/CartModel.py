import uuid

# Data Base service
from src.services.DataBaseService import DataBaseService

conn = DataBaseService()


class CartModel():
    """
    Represents a cart model for an e-commerce application.
    """

    def __init__(self, id, customer_id=None, product_id=None, quantity=None, name=None, price=None, total=None):
        """
        id (str): The unique identifier of the cart.
        customer_id (str): The unique identifier of the customer associated with the cart.
        product_id (str): The unique identifier of the product in the cart.
        quantity (int): The quantity of the product in the cart.
        name (str): The name of the product in the cart.
        price (float): The price of the product in the cart.
        total (float): The total price of the products in the cart.
        """
        self.id = id if id is not None else str(uuid.uuid4())
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.name = name
        self.price = price
        self.total = total

    def add(self):
        """
        Adds a product to the cart.

        Returns:
            bool: True if the product was successfully added, False otherwise.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc(
                "Add_to_cart", (self.product_id, self.customer_id, self.quantity, self.id))
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
    def get(cls, user_id):
        """
        Retrieves the cart for a specific user.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            list: A list of cart items for the user.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Get_cart", (user_id,))
            for results in cursor.stored_results():
                cart = results.fetchall()
            if cart:
                return cart
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def remove(cls, user_id, product_id):
        """
        Removes a product from the cart.

        Args:
            user_id (str): The unique identifier of the user.
            product_id (str): The unique identifier of the product.

        Returns:
            bool: True if the product was successfully removed, False otherwise.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Remove_to_cart", (user_id, product_id))
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
    def empty(cls, user_id):
        """
        Empties the cart for a specific user.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            bool: True if the cart was successfully emptied, False otherwise.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Empty_cart", (user_id,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'success':
                conn.connection.commit()
                return True
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def to_dict(self):
        """
        Converts the cart model to a dictionary representation.

        Returns:
            dict: A dictionary representation of the cart model.
        """
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'total': self.total
        }

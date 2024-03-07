
class Cart:
    """
    Class representing a shopping cart item.

    Attributes:
        id (str): unique identifier of the cart item.
        customer_id (str): ID of the customer to which the cart item belongs.
        product_id (str): ID of the product in the cart item.
        quantity (int): Quantity of the product in the cart item.
    """

    def __init__(self, **kwargs):
        """
        Initializes an object of type Cart.

        Args:
            **kwargs: key-value arguments to initialize the attributes of the cart element.
        """
        self.id = kwargs.get('id')
        self.customer_id = kwargs.get('customer_id')
        self.product_id = kwargs.get('product_id')
        self.quantity = kwargs.get('quantity')

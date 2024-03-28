class OrderDetails():
    """
    The 'OrderDetails' class represents the details of an order.

    Attributes:
        id (str): The unique identifier of the order.
        order_number (str): The order number associated with the order.
        total_quantity (int): The total quantity of items in the order.
        total_amount (float): The total amount of the order.

    Methods:
        to_dict(): Returns a dictionary representation of the order details.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.order_number = kwargs.get('order_number')
        self.total_quantity = kwargs.get('total_quantity')
        self.total_amount = kwargs.get('total_amount')

    def to_dict(self):
        data = {
            "id": self.id,
            "order_number": self.order_number,
            "total_quaintity": self.total_quantity,
            "total_amount": self.total_amount
        }
        return {key: value for key, value in data.items() if value is not None}

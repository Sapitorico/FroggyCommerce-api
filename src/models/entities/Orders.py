class Order():
    """
    The 'Order' class represents an order in a system. It contains information about the order, such as the order ID, customer ID, address ID, payment ID, details ID, status, and payment status.

    Attributes:
        id (str): The ID of the order.
        customer_id (str): The ID of the customer who placed the order.
        address_id (str): The ID of the address associated with the order.
        payment_id (str): The ID of the payment method used for the order.
        details_id (str): The ID of the order details.
        status (str): The status of the order.
        payment_status (str): The payment status of the order.

    Methods:
        to_dict(): Converts the order object into a dictionary.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.customer_id = kwargs.get('customer_id')
        self.address_id = kwargs.get('address_id')
        self.payment_id = kwargs.get('payment_id')
        self.details_id = kwargs.get('details_id')
        self.status = kwargs.get('status')
        self.payment_status = kwargs.get('payment_status')

    def to_dict(self):
        data = {
            "id": self.id,
            "customer_id": self.customer_id,
            "address_id": self.address_id,
            "payment_id": self.payment_id,
            "details_id": self.details_id,
            "status": self.status,
            "payment_status": self.payment_status,
        }
        return {key: value for key, value in data.items() if value is not None}

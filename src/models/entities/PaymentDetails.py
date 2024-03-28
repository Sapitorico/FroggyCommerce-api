class PaymentDetails():
    """
    The PaymentDetails class represents the details of a payment.

    Attributes:
        id (str): The unique identifier of the payment.
        amount (float): The amount of the payment.
        status (str): The status of the payment.

    Methods:
        __init__(self, **kwargs): Initializes a new instance of the PaymentDetails class.
        to_dict(self): Converts the PaymentDetails object to a dictionary.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.amount = kwargs.get('amount')
        self.status = kwargs.get('status')

    def to_dict(self):
        data = {
            "id": self.id,
            "amount": self.amount,
            "status": self.status,
        }
        return {key: value for key, value in data.items() if value is not None}

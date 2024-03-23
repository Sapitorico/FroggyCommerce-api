class PaymentDetails():

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.order_id = kwargs.get('order_id')
        self.amount = kwargs.get('amount')
        self.status = kwargs.get('status')
        self.method = kwargs.get('method')

    def to_dict(self):
        data = {
            "id": self.id,
            "order_id": self.order_id,
            "amount": self.amount,
            "status": self.status,
            "method": self.method
        }
        return {key: value for key, value in data.items() if value is not None}

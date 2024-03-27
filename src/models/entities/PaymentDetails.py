class PaymentDetails():

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

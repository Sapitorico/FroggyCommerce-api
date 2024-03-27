class Order():

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

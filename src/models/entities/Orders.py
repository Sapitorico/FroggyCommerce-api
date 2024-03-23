class Order():

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.customer_id = kwargs.get('customer_id')
        self.order_date = kwargs.get('order_date')
        self.status = kwargs.get('status')

    def to_dict(self):
        data = {
            "id": self.id,
            "customer_id": self.customer_id,
            "order_date": self.order_date,
            "status": self.status,
        }
        return {key: value for key, value in data.items() if value is not None}

class OrderDetails():

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.order_id = kwargs.get('order_id')
        self.prodcut_id = kwargs.get('product_id')
        self.status = kwargs.get('status')
        self.quantity = kwargs.get('quantity')
        self.unit_price = kwargs.get('unit_price')
        self.total_price = kwargs.get('total_price')

    def to_dict(self):
        data = {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "status": self.status,
            "quaintity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price
        }
        return {key: value for key, value in data.items() if value is not None}

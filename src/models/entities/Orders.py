class Order():
    
    def __init__(self, id, customer_id, order_date, status, created_at, updated_at):
        self.id = id
        self.customer_id = customer_id
        self.order_date = order_date
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

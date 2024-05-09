import uuid

# Data Base Service
from src.services.DataBaseService import DataBaseService

conn = DataBaseService()

class OrderModel():
    def __init__(self, customer_id, address_id, order_number, total_quantity, total_amount):
        self.id = str(uuid.uuid4())
        self.customer_id = customer_id
        self.address_id = address_id
        self.order_details_id = str(uuid.uuid4())
        self.order_number = order_number
        self.total_quantity = total_quantity
        self.total_amount = total_amount
        self.payment_id = str(uuid.uuid4())

    def create(self, merchant_order):
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Create_order_details", (self.order_details_id, self.order_number,
                                                     self.total_quantity, self.total_amount,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'order_exists':
                return None
            for item in merchant_order['items']:
                item_id = str(uuid.uuid4())
                product_id = item['id']
                quantity = item['quantity']
                unit_price = item['unit_price']
                cursor.callproc("Create_order_item",
                                (item_id, self.order_details_id, product_id, quantity, unit_price,))
                for result in cursor.stored_results():
                    result.fetchone()[0]
            cursor.callproc("Create_payment_details",
                            (self.payment_id, self.total_amount, 'paid',))
            cursor.callproc(
                "Create_order", (self.id, self.customer_id, self.address_id, self.payment_id,
                                 self.order_details_id, self.order_number, 'paid',))
            conn.connection.commit()
            return True
        except Exception as e:
            print("error", str(e))
        finally:
            conn.close()

import uuid

from flask import json

# Data Base Service
from src.services.DataBaseService import DataBaseService

conn = DataBaseService()


class OrderModel():
    def __init__(self, customer_id, address_id, order_number, total_quantity, total_amount):
        self.customer_id = customer_id
        self.address_id = address_id
        self.order_number = order_number
        self.total_quantity = total_quantity
        self.total_amount = total_amount

    def create(self, merchant_order):
        try:
            cursor = conn.get_cursor()
            items_json = json.dumps(merchant_order['items'])
            cursor.callproc(
                "Create_order", (self.order_number, self.total_quantity, self.total_amount, items_json,
                                 self.customer_id, self.address_id, 'paid',))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'order_exists':
                return None
            conn.connection.commit()
            return True
        except Exception as e:
            print("error", str(e))
        finally:
            conn.close()

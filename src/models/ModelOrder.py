from flask import jsonify
import uuid


class ModelOrder():

    @classmethod
    def generate_order(cls, db, user_id, address_id, merchant_order):
        cursor = db.cursor()
        try:
            order_id = str(uuid.uuid4())
            order_details_id = str(uuid.uuid4())
            payment_id = str(uuid.uuid4())
            total_quantity = sum(item['quantity']
                                 for item in merchant_order['items'])
            cursor.callproc("Create_order_details", (order_details_id,
                            merchant_order['id'], total_quantity, merchant_order['total_amount'],))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'order_exists':
                print("la order ya existe")
                return None
            for item in merchant_order['items']:
                item_id = str(uuid.uuid4())
                product_id = item['id']
                quantity = item['quantity']
                unit_price = item['unit_price']
                cursor.callproc("Create_order_item",
                                (item_id, order_details_id, product_id, quantity, unit_price,))
                for result in cursor.stored_results():
                    result.fetchone()[0]
            cursor.callproc("Create_payment_details",
                            (payment_id, merchant_order['total_amount'], 'paid',))
            cursor.callproc(
                "Create_order", (order_id, user_id, address_id, payment_id, order_details_id, merchant_order['id'], 'paid',))
            db.commit()
            return jsonify({"success": True, "message": "Order created successfully"}), 201
        except Exception as e:
            print("error", str(e))
        finally:
            cursor.close()

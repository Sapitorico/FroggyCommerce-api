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
            total_quantity = 0
            for item in merchant_order['items']:
                total_quantity += item['quantity']
            cursor.callproc("Create_order_details", (order_details_id,
                            merchant_order['id'], total_quantity, merchant_order['total_amount'],))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'order_exists':
                print("la order ya existe")
                return jsonify({"success": False, "message": "Order already exists"}), 400
            cursor.callproc("Create_payment_details",
                            (payment_id, merchant_order['total_amount'], 'paid',))
            cursor.callproc(
                "Create_order", (order_id, user_id, address_id, payment_id, order_details_id, merchant_order['id'], 'paid',))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'order_not_exist':
                db.rollback()
                return jsonify({"success": False, "message": "Order does not exist"}), 400
            db.commit()
            return jsonify({"success": True, "message": "Order created successfully"}), 201
        except Exception as e:
            print("error", str(e))
        finally:
            cursor.close()

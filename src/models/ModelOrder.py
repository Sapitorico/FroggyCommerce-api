from flask import jsonify
import uuid


class ModelOrder():

    @classmethod
    def generate_order(cls, db, user_id, address_id, merchant_order):
        try:
            cursor = db.cursor()
            cursor.callproc(
                "Create_order", (merchant_order['id'], user_id, address_id,))
            print(merchant_order)
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'order_exists':
                print("la order ya existe")
            elif message == 'success':
                print("orden creada")
            order_details_id = str(uuid.uuid4())
            for item in merchant_order['items']:
                product_id = item['id']
                quantity = item['quantity']
            cursor.callproc("Create_order_details", (order_details_id,
                            merchant_order['id'], product_id, quantity, merchant_order['total_amount'],))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'order_not_exist':
                print("la order no existe")
                db.rollback()
            if message == 'order_details_exists':
                print("el detalle de order ya existe")
                db.rollback()
            elif message == 'success':
                print("detalles de orden creados")
                db.commit()
            for payment in merchant_order['payments']:
                payment_id = payment['id']
            cursor.callproc("Crate_payment_details",
                            (payment_id, order_details_id, merchant_order['total_amount'],))
        except Exception as e:
            print("error", str(e))
        finally:
            cursor.close()

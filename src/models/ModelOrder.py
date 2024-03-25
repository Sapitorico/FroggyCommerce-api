from flask import jsonify
import uuid


class ModelOrder():

    @classmethod
    def generate_order(cls, db, user_id, address_id, merchant_order):
        try:
            cursor = db.cursor()
            cursor.callproc(
                "Crate_order", (merchant_order['id'], user_id, address_id,))
            # order_details_id = str(uuid.uuid4())
            # for item in payment_info['additional_info']['items']:
            #     product_id = item['id']
            #     quantity = item['quantity']
            #     unit_price = item['unit_price']
            # cursor.callproc("Crate_order_details", (order_details_id,
            #                 merchant_order['id'], product_id, quantity, unit_price, payment_info['transaction_amount'],))
            # cursor.callproc("Crate_payment_details",
            #                 (payment_info['id'], order_details_id, payment_info['transaction_amount'],))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                print("el usuairo no existe o la direccion no existe")
            if message == 'order_exists':
                print("la order ya existe")
            elif message == 'success':
                db.commit()
                print("ordencreada")
        except Exception as e:
            print("error", str(e))
        finally:
            cursor.close()

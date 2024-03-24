from flask import jsonify
import uuid


class ModelOrder():

    @classmethod
    def generate_order(cls, db, user_id, address_id, merchant_order, payment_info):
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
                message = result.fetchone()
            if message == 'not_exist':
                print("el usuairo no existe o la direccion no existe")
            elif message == 'success':
                db.commit()
                print("ordencreada")
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            cursor.close()

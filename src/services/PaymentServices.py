from flask import jsonify
import os

# Mercado Pago sdk
from src.utils.MercadoPagoSDK import MP_SDK

# Entities
from src.models.entities.Orders import Order
from src.models.entities.OrderDetails import OrderDetails
from src.models.entities.PaymentDetails import PaymentDetails


class PaymentServices():

    @classmethod
    def generate_preference(cls, db, user_id, address_id):
        try:
            cursor = db.cursor()
            cursor.callproc("Get_cart", (user_id,))
            for results in cursor.stored_results():
                result = results.fetchall()
            if not result:
                return jsonify({"success": False, "message": "The cart is empty"}), 400
            cart = []
            for item in result:
                cart.append({
                    "id": item[0],
                    "title": item[1],
                    "currency_id": "UYU",
                    "unit_price": float(item[2]),
                    "quantity": item[3],
                })
            preference_data = cls.generate_preference_data(
                cart, user_id, address_id)
            preference_response = MP_SDK().sdk.preference().create(preference_data)
            preference = preference_response["response"]['init_point']
            return jsonify({"success": True, "message": "Payment initiated successfully", "payment_link": preference}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def verify_payment(cls, topic, payment_id):
        merchant_order = None
        if topic == 'payment':
            payment_info_response = MP_SDK().sdk.payment().get(payment_id)
            if payment_info_response['status'] == 200:
                order_id = payment_info_response["response"]["order"]["id"]
                merchant_order_response = MP_SDK().sdk.merchant_order().get(order_id)
                merchant_order = merchant_order_response["response"]
        elif topic == 'merchant_order':
            merchant_order_response = MP_SDK().sdk.merchant_order().get(payment_id)
            if merchant_order_response['status'] == 200:
                merchant_order = merchant_order_response["response"]

        paid_amount = 0
        if merchant_order:
            for payment in merchant_order.get('payments', []):
                if payment.get('status') == 'approved':
                    paid_amount += payment.get('transaction_amount', 0)

            if paid_amount >= merchant_order.get('total_amount', 0):
                if len(merchant_order.get('shipments', [])) > 0:
                    if merchant_order['shipments'][0].get('status') == "ready_to_ship":
                        print(
                            "Totalmente pagado. Imprima la etiqueta y libere su artículo.")
                else:
                    print("Totalmente pagado. Libere su artículo.")
            else:
                print("Aún no ha pagado. No libere su artículo.")

        return merchant_order

    @classmethod
    def verify_user_by_id(cls, db, user_id):
        try:
            cursor = db.cursor()
            cursor.callproc("User_by_id", (user_id,))
            for result in cursor.stored_results():
                user = result.fetchone()
            if not user:
                return jsonify({"success": False, "message": "User not found"}), 404
            cursor.close()
            return None
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500

    @classmethod
    def verify_address(cls, db, address_id):
        try:
            cursor = db.cursor()
            cursor.callproc("Get_address", (address_id,))
            for result in cursor.stored_results():
                address = result.fetchone()
            if not address:
                return jsonify({"success": False, "message": "Address not found"}), 404
            return None
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            cursor.close()

    @staticmethod
    def generate_preference_data(cart, user_id, address_id):
        base_url = os.getenv('BASE_URL')
        preference_data = {
            "items": cart,
            "back_urls": {
                "success": f"http://localhost:5000/api/payment/success",
                "failure": f"http://localhost:5000/api/payment/failure",
                "pending": f"http://localhost:5000/api/payment/pending"
            },
            "notification_url": f"https://79f6-167-58-246-194.ngrok-free.app/api/payment/notification/{user_id}/{address_id}",
            "statement_descriptor": "E-commerce-sapardo",
        }
        return preference_data

from flask import jsonify
from datetime import datetime
import uuid

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
            preference_data = {
                "items": cart,
                "back_urls": {
                    "success": "http://localhost:5000/api/payment/success",
                    "failure": "http://localhost:5000/api/payment/failure",
                    "pending": "http://localhost:5000/api/payment/pending"
                },
                "notification_url": f"https://0736-190-134-51-57.ngrok-free.app/api/payment/notification/{user_id}/{address_id}",
                "statement_descriptor": "E-commerce-sapardo",
            }
            preference_response = MP_SDK().sdk.preference().create(preference_data)
            preference = preference_response["response"]['init_point']
            return jsonify({"success": True, "message": "Payment initiated successfully", "payment_link": preference}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def notifications(cls, db, topic, id, user_id, address_id):
        if topic == 'payment':
            payment_info_response = MP_SDK().sdk.payment().get(id)
            merchant_order_response = MP_SDK().sdk.merchant_order().get(
                payment_info_response["response"]['order']['id'])

            if payment_info_response and payment_info_response['status'] == 200:
                payment_info = payment_info_response["response"]

            if merchant_order_response and merchant_order_response['status'] == 200:
                merchant_order = merchant_order_response["response"]

            paid_amount = None
            total_amount = None
            if 'status' in payment_info and payment_info['status'] == 'approved':
                paid_amount = payment_info['transaction_amount']
            if 'status' in merchant_order and merchant_order['status'] == 'closed':
                total_amount = merchant_order['total_amount']

            if paid_amount and total_amount and paid_amount >= total_amount:
                print("Totalmente pagado. Imprima la etiqueta y libere su artículo")
                print("Payment ID:", payment_info['id'])
                print("Status:", payment_info['status'])
                print("Transaction Amount:",
                      payment_info['transaction_amount'])
                product_id = None
                quantity = None
                unit_price = None
                for item in payment_info['additional_info']['items']:
                    product_id = item['id']
                    quantity = item['quantity']
                    unit_price = item['unit_price']
                order = Order(
                    id=merchant_order['id'],
                    customer_id=user_id,
                    address_id=address_id,
                    order_date=datetime.now(),
                    status="processing",
                )
                order_details_id = str(uuid.uuid4())
                order_details = OrderDetails(
                    id=order_details_id ,
                    order_id=merchant_order['id'],
                    product_id=product_id,
                    status="paid",
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=payment_info['transaction_amount']
                )
                payment_details = PaymentDetails(
                    id=payment_info['id'],
                    order_id=order_details_id,
                    amount=payment_info['transaction_amount'],
                    status="completed",
                    method="Mercado Pago"
                )
            else:
                print("Aún no ha pagado. No libere su artículo")
                
            return None

    @classmethod
    def verify_user_by_id(cls, db, id):
        try:
            cursor = db.cursor()
            cursor.callproc("User_by_id", (id,))
            for result in cursor.stored_results():
                user = result.fetchone()
            if not user:
                return jsonify({"success": False, "message": "User not found"}), 404
            return None
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @staticmethod
    def validate(data):
        """
        Validate the payment method data.

        Parameters:
        - data (dict): A dictionary containing the payment method data.

        Returns:
        - None: If the data is valid.

        Raises:
        - JSONifyError: If no data is provided.
        - JSONifyError: If the 'method' field is missing.
        - JSONifyError: If the 'method' is not 'Mercado Pago'.

        """
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        if 'method' not in data:
            return jsonify({"success": False, "message": "'method' field is required"}), 400
        elif data['method'] not in ['Mercado Pago']:
            return jsonify({"success": False, "message": "'method' must be either 'Mercado Pago'"}), 400

        return None

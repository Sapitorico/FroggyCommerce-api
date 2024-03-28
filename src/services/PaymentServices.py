from flask import jsonify
import os

# Mercado Pago sdk
from src.utils.MercadoPagoSDK import MP_SDK


class PaymentServices():
    """
    This class provides methods for generating payment preferences.
    It interacts with the Mercado Pago SDK to perform these operations.
    """

    @classmethod
    def generate_preference(cls, db, user_id, address_id):
        """
        Generates a payment preference for a user.

        This method interacts with the Mercado Pago SDK to generate a payment preference based on the user's cart, user ID, and address ID. It retrieves the cart items from the database, converts them into the required format, and creates a preference using the Mercado Pago SDK. The preference is then returned as a JSON response.

        Parameters:
            db (database connection): The database connection object.
            user_id (str): The ID of the user.
            address_id (str): The ID of the address.

        Returns:
            JSON response: A JSON response containing the success status, message, and payment link.
        """
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
        """
        Verifies the payment status and provides information about the payment.

        This method interacts with the Mercado Pago SDK to verify the payment status based on the topic and payment ID provided. It retrieves the payment information and the associated merchant order information using the Mercado Pago SDK. It then calculates the total paid amount and compares it with the total amount of the merchant order. Depending on the payment status and the shipment status, it prints a message indicating whether the payment is fully paid or not.

        Parameters:
            topic (str): The topic of the payment. It can be either 'payment' or 'merchant_order'.
            payment_id (str): The ID of the payment or merchant order.

        Returns:
            dict or None: The merchant order information if available, otherwise None.
        """
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
        """
        Verifies the existence of a user based on the user ID.

        Parameters:
            db (database connection): The database connection object.
            user_id (str): The ID of the user.
        """
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
        """
        Verifies the existence of an address based on the address ID.

        Parameters:
            db (database connection): The database connection object.
            address_id (str): The ID of the address.
        """
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
        """
        This class provides methods for generating payment preferences.
        It interacts with the Mercado Pago SDK to perform these operations.
        """
        base_url = os.getenv('BASE_URL')
        preference_data = {
            "items": cart,
            "back_urls": {
                "success": f"http://localhost:5000/api/payment/success",
                "failure": f"http://localhost:5000/api/payment/failure",
                "pending": f"http://localhost:5000/api/payment/pending"
            },
            "notification_url": f"{base_url}/api/payment/notification/{user_id}/{address_id}",
            "statement_descriptor": "E-commerce-sapardo",
        }
        return preference_data

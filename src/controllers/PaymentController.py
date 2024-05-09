import os
from flask import jsonify

# Models
from src.models.OrderModel import OrderModel
from src.models.AddressModel import AddressModel
from src.models.CartModel import CartModel
from src.models.UsersModel import UsersModel

# Services
from src.services.DataBaseService import DataBaseService
from src.services.MercadoPagoService import MP_SDK

conn = DataBaseService()


class PaymentController():

    @classmethod
    def generate_preference(cls, user_id, address_id):
        """
        Generates a payment preference for the given user and address.

        Args:
            user_id (str): The ID of the user.
            address_id (str): The ID of the address.

        Returns:
            tuple: A tuple containing the JSON response and the HTTP status code.
                The JSON response contains the success status, a message, and the payment link.
                The HTTP status code indicates the success or failure of the payment initiation.
        """
        address = AddressModel.get_by_id(address_id)
        if not address:
            return jsonify({"success": False, "message": "Address not found"}), 404
        cart_result = CartModel.get(user_id)
        if not cart_result:
            return jsonify({"success": False, "message": "Cart is empty"}), 404
        cart = []
        for item in cart_result:
            cart.append({
                "id": item[0],
                "title": item[1],
                "currency_id": "UYU",
                "unit_price": float(item[2]),
                "quantity": item[3],
            })
        try:
            preference_data = cls.generate_preference_data(
                cart, user_id, address_id)
            preference_response = MP_SDK().sdk.preference().create(preference_data)
            preference = preference_response["response"]['init_point']
            return jsonify({"success": True, "message": "Payment initiated successfully", "payment_link": preference}), 200
        except Exception as e:
            print(e)
            return jsonify({"success": False, "message": "Error generating payment preference"}), 500

    @classmethod
    def generate_order(cls, user_id, address_id, topic, payment_id):
        """
        Generates an order for a user based on the provided parameters.

        Args:
            user_id (str): The ID of the user placing the order.
            address_id (str): The ID of the address for the order.
            topic (str): The topic of the payment.
            payment_id (str): The ID of the payment.

        Returns:
            tuple: A tuple containing the JSON response and the HTTP status code.
                The JSON response contains a success flag and a message.
                The HTTP status code indicates the success or failure of the operation.
        """
        user = UsersModel.get_by_id(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        address = AddressModel.get_by_id(address_id)
        if not address:
            return jsonify({"success": False, "message": "Address not found"}), 404
        merchant_order = cls.verify_payment(topic, payment_id)
        if merchant_order:
            total_quantity = sum(item['quantity']
                                 for item in merchant_order['items'])
            order = OrderModel(customer_id=user_id, address_id=address_id, order_number=merchant_order['id'],
                               total_quantity=total_quantity, total_amount=merchant_order['total_amount'])
            response = order.create(merchant_order)
            if response:
                CartModel.empty(user_id)
        return jsonify({"success": True, "message": "Order created successfully"}), 200

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

    @staticmethod
    def generate_preference_data(cart, user_id, address_id):
        """
        This class provides methods for generating payment preferences.
        It interacts with the Mercado Pago SDK to perform these operations.
        """
        name = os.getenv('API_NAME')
        usr_schema = os.getenv('URL_SCHEME')
        server_name = os.getenv('SERVER_NAME')
        preference_data = {
            "items": cart,
            "back_urls": {
                "success": f"{usr_schema}://{server_name}/api/payment/success",
                "failure": f"{usr_schema}://{server_name}/api/payment/failure",
                "pending": f"{usr_schema}://{server_name}/api/payment/pending"
            },
            "notification_url": f"{usr_schema}://{server_name}/api/payment/notification/{user_id}/{address_id}",
            "statement_descriptor": name,
        }
        return preference_data

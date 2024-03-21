

from flask import jsonify


class PaymentServices():

    @classmethod
    def mercado_pago(cls, db, sdk, user_id):
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
                "notification_url": f"https://0736-190-134-51-57.ngrok-free.app/api/payment/notification/{user_id}",
                "statement_descriptor": "E-commerce-sapardo",
            }
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]['init_point']
            return jsonify({"success": True, "message": "Payment initiated successfully", "payment_link": preference}), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        finally:
            cursor.close()

    @staticmethod
    def validate(data):
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        if 'method' not in data:
            return jsonify({"success": False, "message": "'method' field is required"}), 400
        elif data['method'] not in ['Mercado Pago']:
            return jsonify({"success": False, "message": "'method' must be either 'Mercado Pago'"}), 400

        return None

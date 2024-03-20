import mercadopago
import os


class PaymentServices():

    @classmethod
    def mercado_pago(cls):
        sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))
        preference_data = {
            "items": [
                {
                    "id": "item-ID-1234",
                    "title": "Mi producto",
                    "currency_id": "UYU",
                    "picture_url": "https://www.mercadopago.com/org-img/MP3/home/logomp3.gif",
                    "description": "Descripción del Item",
                    "category_id": "art",
                    "quantity": 1,
                    "unit_price": 75.76
                }
            ],
            "back_urls": {
                "success": "http://localhost:5000/api/payment/success",
            },
            "notification_url": "https://35ec-167-58-253-46.ngrok-free.app/api/payment/notification",
        }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]['init_point']
        return preference

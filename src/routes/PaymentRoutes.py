from flask import Blueprint, request

# Security
from src.utils.Security import Security

# Services
from src.services.PaymentServices import PaymentServices

# Mercado Pago sdk
from src.utils.MercadoPagoSDK import MP_SDK

# Database connection
from src.database.db_conection import DBConnection

db = DBConnection()

payment = Blueprint('payment', __name__)

sdk = MP_SDK().sdk


@payment.route('/generate', methods=['POST'])
@Security.verify_session
def generate_payment_link(user_id):
    if request.method == 'POST':
        data = request.json
        valid_data = PaymentServices.validate(data)
        if valid_data:
            return valid_data
    response = PaymentServices.mercado_pago(db.connection, sdk, user_id)
    return response


@payment.route('/success', methods=['GET'])
def payment_success():
    return "success"


@payment.route('/pending', methods=['GET'])
def payment_pending():
    return "pending"


@payment.route('/failure', methods=['GET'])
def payment_failure():
    return "failure"


@payment.route('/notification/<string:id>', methods=['POST'])
def notification(id):
    # Obtener parámetros de consulta
    topic = request.args.get('topic')
    id = request.args.get('id')

    if topic == 'payment':
        # Obtener los datos de pago
        payment_info_response = sdk.payment().get(id)
        merchant_order_response = sdk.merchant_order().get(
            payment_info_response["response"]['order']['id'])

        # Imprimir información específica
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
            print("Transaction Amount:", payment_info['transaction_amount'])
            for item in payment_info['additional_info']['items']:
                print(item['id'])
        else:
            print("Aún no ha pagado. No libere su artículo")
    else:
        pass

    return "Received", 200

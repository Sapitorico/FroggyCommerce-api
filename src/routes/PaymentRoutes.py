from flask import Blueprint, request
import mercadopago
import os
import json


# Security
from src.utils.Security import Security

# Services
from src.services.payment_services import PaymentServices

payment = Blueprint('payment', __name__)

sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))


@payment.route('/generate', methods=['GET'])
@Security.verify_session
def generate_payment_link(user_id):
    response = PaymentServices.mercado_pago()
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


@payment.route('/notification', methods=['POST'])
def notification():
    # Obtener parámetros de consulta
    topic = request.args.get('topic')
    id = request.args.get('id')

    print(f"Topic: {topic}, ID: {id}")

    # Obtener los datos de pago
    payment_info = sdk.payment().get(id)

    if topic == 'payment':
        # Obtener los datos de pago
        payment_info = sdk.payment().get(id)
        if payment_info["status"] == 200:
            payment_data = payment_info["response"]
            # Imprimir los datos de pago de forma bonita
            print(json.dumps(payment_data, indent=4))
        else:
            print(
                f"Error al obtener los datos de pago: {payment_info['status']}")
    elif topic == 'merchant_order':
        # Obtener los datos de la orden
        order_info = sdk.merchant_order().get(id)
        if order_info["status"] == 200:
            order_data = order_info["response"]
            # Imprimir los datos de la orden de forma bonita
            print(json.dumps(order_data, indent=4))
        else:
            print(
                f"Error al obtener los datos de la orden: {order_info['status']}")

    return "Received", 200

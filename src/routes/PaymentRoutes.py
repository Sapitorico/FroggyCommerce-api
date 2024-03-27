from flask import Blueprint, request
from datetime import datetime

# Models
from src.models.ModelOrder import ModelOrder
from src.models.ModelCart import ModelCart

# Security
from src.utils.Security import Security

# Services
from src.services.PaymentServices import PaymentServices


# Database connection
from src.database.db_conection import DBConnection

db = DBConnection()

payment = Blueprint('payment', __name__)


@payment.route('/generate/<string:address_id>', methods=['GET'])
@Security.verify_session
def generate_payment_link(user_id, address_id):
    """
    Generates a payment link for a given user and address.

    Parameters:
    - user_id (str): The ID of the user.
    - address_id (str): The ID of the address.

    Returns:
    - dict: A JSON response containing the success status, message, and payment link.

    """
    if request.method == 'GET':
        response = PaymentServices.verify_address(db.connection, address_id)
        if response:
            return response
        response = PaymentServices.generate_preference(
            db.connection, user_id, address_id)
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


@payment.route('/notification/<string:user_id>/<string:address_id>', methods=['POST'])
def notification(user_id, address_id):
    """
    Handle the notification endpoint for payment processing.

    Args:
        user_id (str): The ID of the user.
        address_id (str): The ID of the address.

    Returns:
        str: The response message indicating the status of the notification.
    """
    if request.method == 'POST':
        response = PaymentServices.verify_user_by_id(db.connection, user_id)
        if response:
            return response
        response = PaymentServices.verify_address(db.connection, address_id)
        if response:
            return response
        topic = request.args.get('topic')
        payment_id = request.args.get('id')
        merchant_order = PaymentServices.verify_payment(
            topic, payment_id)
        if merchant_order:
            response = ModelOrder.generate_order(
                db.connection, user_id, address_id, merchant_order)
            if response:
                ModelCart.empty_cart(db.connection, user_id)
    return "Received", 200

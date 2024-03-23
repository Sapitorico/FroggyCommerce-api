from flask import Blueprint, request

# Security
from src.utils.Security import Security

# Services
from src.services.PaymentServices import PaymentServices


# Database connection
from src.database.db_conection import DBConnection

db = DBConnection()

payment = Blueprint('payment', __name__)


@payment.route('/generate', methods=['POST'])
@Security.verify_session
def generate_payment_link(user_id):
    if request.method == 'POST':
        data = request.json
        valid_data = PaymentServices.validate(data)
        if valid_data:
            return valid_data
    response = PaymentServices.generate_preference(db.connection, user_id)
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
    if request.method == 'POST':
        response = PaymentServices.verify_user_by_id(db.connection, user_id)
        if response:
            return response
        topic = request.args.get('topic')
        payment_id = request.args.get('id')
        payment = PaymentServices.notifications(
            db.connection, topic, payment_id, user_id, address_id)

    return "Received", 200

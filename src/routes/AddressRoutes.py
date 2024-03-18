from flask import Blueprint, request

# Models
from src.models.ModelAddress import ModelAddress

# Entities
from src.models.entities.Address import Address

# Security
from src.utils.Security import Security

# Database
from src.database.db_conection import DBConnection

# Database connection:
db = DBConnection()

address = Blueprint('address', __name__)


@address.route('/', methods=['GET'])
@Security.verify_session
def list_addresses(user_id):
    """
    List addresses for a specific user.

    Parameters:
    - user_id (str): The ID of the user whose addresses are to be listed.
    """
    if request.method == 'GET':
        response = ModelAddress.list_addresses(db.connection, user_id)
        return response


@address.route('/add', methods=['POST'])
@Security.verify_session
def add_new_address(user_id):
    """
    Add a new address for a user.

    Parameters:
        user_id (str): The unique identifier for the user.
        state (str): The state where the address is located.
        city (str): The city where the address is located.
        address (str): The street address.
    """
    if request.method == 'POST':
        data = request.json
        validation_error = ModelAddress.validate(data)
        if validation_error:
            return validation_error
        address = Address(state=data['state'],
                          city=data['city'],
                          address=data['address'])
        response = ModelAddress.add_address(db.connection, user_id, address)
        return response

@address.route('/<string:id>', methods=['GET'])
@Security.verify_session
def get_address(user_id, id):
    """
    List addresses for a specific user.

    Parameters:
    - user_id (str): The ID of the user whose addresses are to be listed.
    """
    if request.method == 'GET':
        response = ModelAddress.get_address_by_id(db.connection, id)
        return response
from flask import Blueprint, request

# Controllers
from src.controllers.AddressController import AddressController

# Security
from src.utils.Security import Security

address = Blueprint('address', __name__)


@address.route('/add', methods=['POST'])
@Security.verify_session
def add_new_address(user_id):
    """
    Add a new address for the specified user.

    Args:
        user_id (str): The ID of the user.

    Returns:
        dict: The response containing the result of the address addition.
    """
    if request.method == 'POST':
        data = request.json
        response = AddressController.add_address(user_id, data)
        return response


@address.route('/', methods=['GET'])
@Security.verify_session
def list_addresses(user_id):
    """
    Retrieve a list of addresses for a given user.

    Parameters:
    - user_id (str): The ID of the user.

    Returns:
    - response (dict): The response containing the list of addresses.
    """
    if request.method == 'GET':
        response = AddressController.get_all_addresses(user_id)
        return response


@address.route('/<string:id>', methods=['GET'])
@Security.verify_session
def get_address(user_id, id):
    """
    Get the address with the specified ID.

    Parameters:
    - user_id (str): The ID of the user making the request.
    - id (str): The ID of the address to retrieve.

    Returns:
    - response (dict): The response containing the address information.
    """
    if request.method == 'GET':
        response = AddressController.get_address(id)
        return response


@address.route('/update/<string:id>', methods=['PUT'])
@Security.verify_session
def update_address(user_id, id):
    """
    Update an address for a user.

    Args:
        user_id (str): The ID of the user.
        id (str): The ID of the address to be updated.

    Returns:
        dict: The response containing the result of the address update.
    """
    if request.method == 'PUT':
        data = request.json
        response = AddressController.update_address(id, data)
        return response


@address.route('/delete/<string:id>', methods=['DELETE'])
@Security.verify_session
def delete_address(user_id, id):
    """
    Delete an address.

    Args:
        user_id (str): The ID of the user.
        id (str): The ID of the address to be deleted.

    Returns:
        dict: A dictionary containing the response message.
    """
    if request.method == 'DELETE':
        response = AddressController.delete_address(id)
        return response

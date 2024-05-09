from flask import Blueprint, request

# Controllers
from src.controllers.UsersController import UsersController


# Security
from src.services.SecurityService import SecurityService

user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
@SecurityService.verify_admin
def get_users():
    """
    Retrieves a list of users.

    Returns:
        The response containing the list of users.
    """
    if request.method == 'GET':
        response = UsersController.get_users()
        return response


@user.route('/profile', methods=['GET'])
@SecurityService.verify_session
def get_profile_user(user_id):
    """
    Retrieves the profile of a user by their ID.

    Args:
        user_id (str): The ID of the user.

    Returns:
        dict: The user profile information.

    """
    if request.method == 'GET':
        response = UsersController.get_user_by_id(user_id)
        return response


@user.route('/update', methods=['POST'])
@SecurityService.verify_session
def update_user(user_id):
    """
    Update user information.

    Args:
        user_id (str): The ID of the user to be updated.

    Returns:
        dict: The response containing the result of the update operation.
    """
    if request.method == 'POST':
        data = request.json
        response = UsersController.update_user(user_id, data)
        return response


@user.route('/delete', methods=['DELETE'])
@SecurityService.verify_session
def delete_user(user_id):
    """
    Deletes a user with the given user_id.

    Args:
        user_id (str): The ID of the user to be deleted.

    Returns:
        dict: A dictionary containing the response message.
    """
    if request.method == 'DELETE':
        response = UsersController.delete_user(user_id)
        return response

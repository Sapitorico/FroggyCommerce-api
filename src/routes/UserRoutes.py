from flask import Blueprint, request

# Models:
from src.models.ModelUser import ModelUser

from src.utils.Security import Security


user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
@Security.verify_admin
def get_users():
    """
    Gets the list of users.

    Returns:
        response: HTTP request response with the list of users.
    """
    if request.method == 'GET':
        response = ModelUser.get_users()
        return response


@user.route('/profile', methods=['GET'])
@Security.verify_session
def get_profile_user(user_id):
    """
    Gets the profile of a specific user.

    Args:
        user_id (str): ID of the user whose profile is to be obtained.
    """
    if request.method == 'GET':
        response = ModelUser.get_user_by_id(user_id)
        return response


@user.route('/update', methods=['POST'])
@Security.verify_session
def update_user(user_id):
    """
    Updates a user's information.

    Args:
        user_id (str): ID of the user whose information is to be updated.
    """
    if request.method == 'POST':
        data = request.json
        valid_data = ModelUser.validate(data)
        if valid_data:
            return valid_data
        response = ModelUser.update_user(user_id, data)
        return response


@user.route('/delete', methods=['DELETE'])
@Security.verify_session
def delete_user(user_id):
    """
    Deletes a user.

    Args:
        user_id (str): ID of the user to be deleted.
    """
    if request.method == 'DELETE':
        response = ModelUser.delete_user(user_id)
        return response

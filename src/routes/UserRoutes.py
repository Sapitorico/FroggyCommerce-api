# # Entities
# from src.models.entities.Users import User
# Models:
from src.models.ModelUser import ModelUser
from flask import Blueprint, request


from src.utils.Security import Security


user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
def get_users():
    access_result = Security.verify_admin(request.headers)
    if access_result:
        return access_result
    if request.method == 'GET':
        response = ModelUser.get_users()
        return response


@user.route('/profile', methods=['GET'])
def get_profile_user():
    access_result = Security.verify_session(request.headers)
    if isinstance(access_result, tuple):
        return access_result
    if request.method == 'GET':
        response = ModelUser.get_user_by_id(access_result)
        return response


@user.route('/update', methods=['POST'])
def update_user():
    access_result = Security.verify_session(request.headers)
    if isinstance(access_result, tuple):
        return access_result
    if request.method == 'POST':
        data = request.json
        valid_data = ModelUser.validate_data_update(data)
        if valid_data:
            return valid_data
        response = ModelUser.update_user(access_result, data)
        return response


@user.route('/delete', methods=['DELETE'])
def delete_user():
    access_result = Security.verify_session(request.headers)
    if isinstance(access_result, tuple):
        return access_result
    if request.method == 'DELETE':
        response = ModelUser.delete_user(access_result)
        return response

# # Entities
# from src.models.entities.Users import User
# Models:
from src.models.ModelUser import ModelUser
from flask import Blueprint, request


from src.utils.Security import Security


user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
@Security.verify_admin
def get_users():
    if request.method == 'GET':
        response = ModelUser.get_users()
        return response


@user.route('/profile', methods=['GET'])
@Security.verify_session
def get_profile_user(user_id):
    if request.method == 'GET':
        response = ModelUser.get_user_by_id(user_id)
        return response


@user.route('/update', methods=['POST'])
@Security.verify_session
def update_user(user_id):
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
    if request.method == 'DELETE':
        response = ModelUser.delete_user(user_id)
        return response

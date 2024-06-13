from flask import Blueprint, jsonify, request

# Controllers
from src.controllers.UsersController import UsersController


# Security
from src.services.SecurityService import SecurityService

# Utils
from src.utils.format_validations import validate

user = Blueprint('user', __name__)


@user.route('/', methods=['GET'])
@SecurityService.verify_admin
def get_users():
    """
    Retrieves a list of users.
    """
    if request.method == 'GET':
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=12, type=int)
        name = request.args.get('name', type=str)
        users, total_pages, response = UsersController.get_users(
            page, per_page, name)
        if response == 'success':
            return jsonify({"success": True, "message": "Users recovered successfully", "users": users, "total_pages": int(total_pages)}), 200
        if response == 'not_found':
            return jsonify({"success": False, "message": "Users not available"}), 200
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@user.route('/profile', methods=['GET'])
@SecurityService.verify_session
def get_profile_user(user_id):
    """
    Retrieves the profile of a user by their ID.
    """
    if request.method == 'GET':
        user, response = UsersController.get_user_by_id(user_id)
        if response == 'success':
            return jsonify({'success': True, 'message': 'User fetched successfully', 'user': user}), 200
        if response == 'not_found':
            return jsonify({'success': False, 'message': 'User not found'}), 404
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@user.route('/profile', methods=['PUT'])
@SecurityService.verify_session
def update_user(user_id):
    """
    Update user information.
    """
    if request.method == 'PUT':
        data = request.json
        schema = {
            'full_name': {'type': 'string', 'minWords': 2, 'maxWords': 2, 'required': True},
            'username': {'type': 'string', 'minLength': 1, 'required': True},
            'email': {'type': 'string', 'minLength': 1, 'format': 'email', 'required': True},
            'phone_number': {'type': 'string', 'minLength': 1, 'format': 'digit', 'required': True},
        }
        error = validate(data, schema)
        if error:
            return jsonify({"success": False, "message": error}), 400
        response = UsersController.update_user(user_id, data)
        if response == 'not_exists':
            return jsonify({'success': False, 'message': 'User not found'}), 404
        if response == 'already_exists':
            return jsonify({'success': False, 'message': 'This \'user\' is already registered'}), 409
        if response == 'success':
            return jsonify({'success': True, 'message': 'User successfully updated'}), 200
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@user.route('/profile', methods=['DELETE'])
@SecurityService.verify_session
def delete_user(user_id):
    """
    Deletes a user with the given user_id.
    """
    if request.method == 'DELETE':
        response = UsersController.delete_user(user_id)
        if response == 'not_exists':
            return jsonify({'success': False, 'message': 'User not found'}), 404
        if response == 'success':
            return jsonify({'success': True, 'message': 'User successfully deleted'}), 200
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500

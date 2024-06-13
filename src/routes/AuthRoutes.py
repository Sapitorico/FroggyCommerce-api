from flask import Blueprint, jsonify, request

# Controllers
from src.controllers.UsersController import UsersController

# Services
from src.services.SecurityService import SecurityService

# Utils
from src.utils.format_validations import validate

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    """
    if request.method == 'POST':
        data = request.json
        schema = {
            'full_name': {'type': 'string', 'minWords': 2, 'maxWords': 2, 'required': True},
            'username': {'type': 'string', 'minLength': 1, 'required': True},
            'email': {'type': 'string', 'minLength': 1, 'format': 'email', 'required': True},
            'phone_number': {'type': 'string', 'minLength': 1, 'format': 'digit', 'required': True},
            'password': {'type': 'string', 'minLength': 8, 'required': True},
        }
        error = validate(data, schema)
        if error:
            return jsonify({"success": False, "message": error}), 400
        full_name, response = UsersController.register(data)
        if response == 'success':
            return jsonify({"success": True, "message": f"User '{full_name}' successfully registered"}), 201
        if response == 'already_exists':
            return jsonify({"success": False, "message": "User already registered"}), 409
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500


@auth.route('/login', methods=['POST'])
def login():
    """
    Handle the login request.
    """
    if request.method == 'POST':
        data = request.json
        schema = {
            'email': {'type': 'string', 'minLength': 1, 'format': 'email', 'required': True},
            'password': {'type': 'string', 'minLength': 8, 'required': True},
        }
        error = validate(data, schema)
        if error:
            return jsonify({"success": False, "message": error}), 400
        user, response = UsersController.login(data)
        if response == 'success':
            token = SecurityService.generate_token(user)
            return jsonify({
                "success": True,
                "message": "Successful login",
                "user": user.to_dict(),
                "token": token
            }), 200
        if response == 'not_found':
            return jsonify({"success": False, "message": "Incorrect credentials"}), 400
        if response == 'failure':
            return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500

from flask import Blueprint, request

# Controllers
from src.controllers.UsersController import UsersController

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    This function handles the registration of a new user by receiving a POST request with JSON data.
    The JSON data should contain the necessary information for user registration.

    Returns:
        The response from the AuthController.register() function.
    """
    if request.method == 'POST':
        data = request.json
        response = UsersController.register(data)
        return response


@auth.route('/login', methods=['POST'])
def login():
    """
    Handle the login request.

    This function receives a POST request with JSON data containing the user's credentials.
    It calls the `login` method of the `AuthController` class to authenticate the user.
    The response from the `login` method is returned as the API response.

    Returns:
        The API response as returned by the `login` method of the `AuthController` class.
    """
    if request.method == 'POST':
        data = request.json
        response = UsersController.login(data)
        return response

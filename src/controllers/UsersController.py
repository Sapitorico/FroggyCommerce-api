from flask import jsonify
import re

# Models
from src.models.UsersModel import UsersModel

# Security
from src.services.SecurityService import SecurityService


class UsersController():

    @classmethod
    def register(cls, data):
        """
        Register a new user.

        Args:
            data (dict): A dictionary containing user registration data.

        Returns:
            dict: A JSON response indicating the success or failure of the registration process.

        """
        validation = cls.validaterRegister(data)
        if validation:
            return validation
        auth = UsersModel(None, data['full_name'], data['username'],
                          data['email'], data['phone_number'], data['password'])
        user = auth.create()
        if not user:
            return jsonify({"success": False, "message": "This 'user' is already registered"}), 400
        return jsonify({"success": True, "message": f"User '{user}' successfully registered"}), 201

    @classmethod
    def login(cls, data):
        """
        Logs in a user with the provided credentials.

        Args:
            data (dict): A dictionary containing the user's login data.

        Returns:
            tuple: A tuple containing the JSON response and the HTTP status code.
                The JSON response contains the following keys:
                    - success (bool): Indicates whether the login was successful.
                    - message (str): A message describing the result of the login attempt.
                    - user (dict): A dictionary containing the user's data.
                    - token (str): A token generated for the user.
        """
        validation = cls.validateLogin(data)
        if validation:
            return validation
        user_data = UsersModel.get(data)
        if not user_data:
            return jsonify({"success": False, "message": "Incorrect credentials"}), 400
        user = UsersModel(user_data[0], user_data[1], user_data[2], user_data[3],
                          user_data[4], SecurityService.check_password(
                              user_data[5], data['password']),
                          user_data[6], user_data[7], user_data[8])
        if user.password == False:
            return jsonify({"success": False, "message": "Incorrect credentials"}), 400
        token = SecurityService.generate_token(user)
        response_data = {
            "success": True,
            "message": "Successful login",
            "user": user.to_dict(),
            "token": token
        }
        return jsonify(response_data), 200

    @classmethod
    def get_users(cls):
        """
        Retrieve a list of users from the UsersModel.

        Returns:
            A JSON response containing the list of users if successful, or an error message if no users are found.
        """
        users = UsersModel.get_all()
        if not users:
            return jsonify({"success": False, "message": "No users found"}), 404
        users = [UsersModel(user[0], user[1], user[2], user[3], user[4], None,
                            user[5], user[6], user[7]).to_dict() for user in users]
        return jsonify({"success": True, "message": "Users fetched successfully", "users": users}), 200

    @classmethod
    def get_user_by_id(cls, id):
        """
        Retrieves a user by their ID.

        Args:
            id (str): The ID of the user to retrieve.

        Returns:
            tuple: A tuple containing the user information if found, or a JSON response with an error message if not found.
        """
        user = UsersModel.get_by_id(id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        user = UsersModel(user[0], user[1], user[2], user[3], user[4],
                          None, user[5], user[6], user[7]).to_dict()
        return jsonify({"success": True, "message": "User fetched successfully", "user": user}), 200

    @classmethod
    def update_user(cls, id, data):
        """
        Update a user's information.

        Args:
            id (str): The ID of the user to be updated.
            data (dict): A dictionary containing the updated user data.

        Returns:
            tuple: A tuple containing the response JSON and the HTTP status code.
                    The response JSON will have a "success" field indicating if the update was successful,
                    and a "message" field with a corresponding message.

        """
        validation = cls.validaterRegister(data)
        if validation:
            return validation
        user = UsersModel(id, data['full_name'], data['username'],
                          data['email'], data['phone_number'], data['password'])
        response = user.update()
        if not response:
            return jsonify({"success": False, "message": "User not found"}), 404
        if response == 'already_exists':
            return jsonify({"success": False, "message": "This 'user' is already registered"}), 400
        return jsonify({"success": True, "message": "User successfully updated"}), 200

    @classmethod
    def delete_user(cls, id):
        """
        Deletes a user with the given ID.

        Args:
            id (str): The ID of the user to be deleted.

        Returns:
            tuple: A tuple containing a JSON response and a status code.
                The JSON response contains a success flag and a message.
                The status code indicates the success or failure of the operation.
        """
        response = UsersModel.delete(id)
        if not response:
            return jsonify({"success": False, "message": "User not found"}), 404
        return jsonify({"success": True, "message": "User successfully deleted"}), 200

    @classmethod
    def validateLogin(cls, data):
        """
        Validates the login data.

        Args:
            data (dict): The login data containing email and password.

        Returns:
            tuple: A tuple containing the response JSON and status code.
                    If the data is valid, returns None.

        """
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        validate = cls.validateEmail(data)
        if validate:
            return validate
        validate = cls.validatePassword(data)
        if validate:
            return validate

        return None

    @classmethod
    def validateEmail(cls, data):
        """
        Validates the email field in the given data.

        Args:
            data (dict): The data containing the email field.

        Returns:
            None: If the email is valid.
            Response: If the email is invalid, returns a JSON response with an error message and status code 400.
        """
        if 'email' not in data:
            return jsonify({"success": False, "message": "'email' field is required"}), 400
        elif not isinstance(data['email'], str) or len(data['email']) == 0:
            return jsonify({"success": False, "message": "'email' field must be a non-empty string"}), 400
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return jsonify({"success": False, "message": "Invalid email format"}), 400

            return None

    @classmethod
    def validatePassword(cls, data):
        """
        Validates the password field in the given data.

        Args:
            data (dict): The data containing the password field.

        Returns:
            tuple: A tuple containing the JSON response and the HTTP status code.

        Raises:
            None

        """
        if 'password' not in data:
            return jsonify({"success": False, "message": "'password' field is required"}), 400
        elif not isinstance(data['password'], str) or len(data['password']) == 0:
            return jsonify({"success": False, "message": "'password' field must be a non-empty string"}), 400
        elif len(data['password']) < 8:
            return jsonify({"success": False, "message": "Password must be at least 8 characters long"}), 400

    @classmethod
    def validaterRegister(cls, data):
        """
        Validates the registration data for a user.

        Args:
            data (dict): The registration data.

        Returns:
            tuple: A tuple containing the validation result. If the data is valid, returns None.
                    If the data is invalid, returns a tuple with the error message and status code.
        """
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        if 'full_name' not in data:
            return jsonify({"success": False, "message": "Field 'full_name' is required"}), 400
        elif not isinstance(data['full_name'], str) or len(data['full_name']) == 0:
            return jsonify({"success": False, "message": "Field 'full_name' must be a non-empty string"}), 400
        elif len(data['full_name'].split(' ')) < 2:
            return jsonify({"success": False, "message": "Full name field must contain both first and last name"}), 400

        if 'username' not in data:
            return jsonify({"success": False, "message": "Field 'username' is required"}), 400
        elif not isinstance(data['username'], str) or len(data['username']) == 0:
            return jsonify({"success": False, "message": "Field 'username' must be a non-empty string"}), 400

        validate = cls.validateEmail(data)
        if validate:
            return validate

        if 'phone_number' not in data:
            return jsonify({"success": False, "message": "Field 'phone_number' is required"}), 400
        elif not isinstance(data['phone_number'], str) or len(data['phone_number']) == 0:
            return jsonify({"success": False, "message": "Field 'phone_number' must be a non-empty string"}), 400
        elif not data['phone_number'].isdigit():
            return jsonify({"success": False, "message": "Invalid phone number format"}), 400

        validate = cls.validatePassword(data)
        if validate:
            return validate

        return None

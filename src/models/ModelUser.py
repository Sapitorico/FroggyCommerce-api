import re
import uuid
from flask import jsonify
from datetime import datetime

# Security:
from src.utils.Security import Security

# Entities:
from src.models.entities.Users import User


class ModelUser():
    """
    This class represents a model for managing user data in the database.

    Methods:
        - register(user): Registers a new user in the database.
        - login(user): Logs in a user.
        - get_users(): Retrieves a list of all users.
        - get_user_by_id(id): Retrieves a specific user by their ID.
        - update_user(id, data_user): Updates data for a specific user.
        - delete_user(id): Deletes a specific user.
        - validate(data): Validates the data for creating a new user.
        - validate_login(data): Validates the data for user login.
    """

    @classmethod
    def register(cls, db, user):
        """
        This method registers a new user in the database.

        If the user already exists in the database, the stored procedure will return 'already_exists'.
        If the registration is successful, it will return 'success'.

        Parameters:
            user (User): The User object containing the user's details.

        """
        try:
            cursor = db.cursor()
            user_id = str(uuid.uuid4())
            cursor.callproc(
                "Register", (user_id, user.full_name, user.email, user.password))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'already_exists':
                return jsonify({"success": False, "message": "This 'user' is already registered"}), 400
            elif message == 'success':
                db.commit()
                return jsonify({"success": True, "message": f"User '{user.full_name}' successfully registered"}), 201
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def login(cls, db, user):
        """
        This method is used to log in a user.

        Parameters:
            user (User): a user object containing the user's email and password.
        """
        try:
            cursor = db.cursor()
            cursor.callproc("Login", (user.email,))
            for result in cursor.stored_results():
                existing_user = result.fetchone()
            if not existing_user:
                return jsonify({"success": False, "message": "Incorrect credentials"}), 400
            user = User(id=existing_user[0],
                        full_name=existing_user[1],
                        email=existing_user[2],
                        password=User.check_password(
                            existing_user[3], user.password),
                        user_type=existing_user[4],
                        created_at=existing_user[5],
                        updated_at=existing_user[6])
            if user.password == False:
                return jsonify({"success": False, "message": "Incorrect credentials"}), 400
            token = Security.generate_token(user)
            response_data = {
                "success": True,
                "message": f"Successful login, welcome \'{user.full_name}\'",
                "user": user.to_dict(),
                "token": token
            }
            return jsonify(response_data), 200
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def get_users(cls, db):
        """"
        This method is used to get a list of all users.
        """
        try:
            cursor = db.cursor()
            cursor.callproc(
                "List_customers")
            for result in cursor.stored_results():
                users = result.fetchall()
            users = [User(id=user[0],
                          full_name=user[1],
                          email=user[2],
                          user_type=user[3],
                          created_at=user[4],
                          updated_at=user[5]).to_dict() for user in users]
            return jsonify({"success": True, "message": "Users fetched successfully", "users": users}), 200
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def get_user_by_id(cls, db, id):
        """
        This method is used to get a specific user by their ID.

        Parameters:
            id (str): the ID of the user to get.
        """
        try:
            cursor = db.cursor()
            cursor.callproc("User_by_id", (id,))
            for result in cursor.stored_results():
                user = result.fetchone()
            if not user:
                return jsonify({"success": False, "message": "User not found"}), 404
            user = User(id=user[0],
                        full_name=user[1],
                        email=user[2],
                        user_type=user[3],
                        created_at=user[4],
                        updated_at=user[5]).to_dict()
            return jsonify({"success": True, "message": "User fetched successfully", "user": user}), 200
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def update_user(cls, db, id, data_user):
        """
        This method is used to update data for a specific user.

        Parameters:
            id (str): The ID of the user to be updated.
            data_user (dict): A dictionary containing the new user data.
        """
        try:
            cursor = db.cursor()
            cursor.callproc("Update_user", (id, data_user['full_name'],
                            data_user['email'], User.hash_password(data_user['password'])))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                return jsonify({"success": False, "message": "User not found"}), 404
            elif message == 'success':
                db.commit()
                return jsonify({"success": True, "message": "User successfully updated"}), 200
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def delete_user(cls, db, id):
        """
        This method is used to delete a specific user.

        Parameters:
        id (str): the ID of the user to be deleted.

        """
        try:
            cursor = db.cursor()
            cursor.callproc("Delete_user", (id,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                return jsonify({"success": False, "message": "User not found"}), 404
            elif message == 'success':
                db.commit()
                return jsonify({"success": True, "message": "User successfully deleted"}), 200
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @staticmethod
    def validate(data):
        """
        Validates the data for creating a new user.

        Args:
            data (dict): The data to be validated.
        """
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        if 'full_name' not in data:
            return jsonify({"success": False, "message": "Field 'full_name' is required"}), 400
        elif not isinstance(data['full_name'], str) or len(data['full_name']) == 0:
            return jsonify({"success": False, "message": "Field 'full_name' must be a non-empty string"}), 400
        elif len(data['full_name'].split(' ')) < 2:
            return jsonify({"success": False, "message": "Full name field must contain both first and last name"}), 400

        if 'email' not in data:
            return jsonify({"success": False, "message": "Field 'email' is required"}), 400
        elif not isinstance(data['email'], str) or len(data['email']) == 0:
            return jsonify({"success": False, "message": "Field 'email' must be a non-empty string"}), 400
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return jsonify({"success": False, "message": "Invalid email format"}), 400

        if 'password' not in data:
            return jsonify({"success": False, "message": "Field 'password' is required"}), 400
        elif not isinstance(data['password'], str) or len(data['password']) == 0:
            return jsonify({"success": False, "message": "Field 'password' must be a non-empty string"}), 400
        elif len(data['password']) < 8:
            return jsonify({"success": False, "message": "Password must be at least 8 characters long"}), 400

        return None

    @staticmethod
    def validate_login(data):
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        if 'email' not in data:
            return jsonify({"success": False, "message": "'email' field is required"}), 400
        elif not isinstance(data['email'], str) or len(data['email']) == 0:
            return jsonify({"success": False, "message": "'email' field must be a non-empty string"}), 400
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return jsonify({"success": False, "message": "Invalid email format"}), 400

        if 'password' not in data:
            return jsonify({"success": False, "message": "'password' field is required"}), 400
        elif not isinstance(data['password'], str) or len(data['password']) == 0:
            return jsonify({"success": False, "message": "'password' field must be a non-empty string"}), 400
        elif len(data['password']) < 8:
            return jsonify({"success": False, "message": "Password must be at least 8 characters long"}), 400

        return None

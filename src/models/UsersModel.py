import uuid

# Security
from src.services.DataBaseService import DataBaseService

# Database connection
from src.services.SecurityService import SecurityService

# Database connection:
conn = DataBaseService()


class UsersModel():
    """
    Represents a user in the e-commerce system.

    Attributes:
        id (str): The unique identifier of the user.
        full_name (str): The full name of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        phone_number (str): The phone number of the user.
        password (str, optional): The password of the user. Defaults to None.
        user_type (str, optional): The type of the user. Defaults to None.
        created_at (datetime, optional): The timestamp when the user was created. Defaults to None.
        updated_at (datetime, optional): The timestamp when the user was last updated. Defaults to None.
    """

    def __init__(self, id, full_name, username, email, phone_number, password=None, user_type=None, created_at=None, updated_at=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.full_name = full_name
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = password
        self.user_type = user_type
        self.created_at = created_at
        self.updated_at = updated_at

    def create(self):
        """
        Creates a new user in the database.

        Returns:
            str: The full name of the created user.

        Raises:
            Exception: If an error occurs during the creation process.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc(
                "Register", (self.id, self.full_name, self.username, self.email,
                             self.phone_number, SecurityService.hash_password(self.password)))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'success':
                conn.connection.commit()
                return self.full_name
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get(cls, data):
        """
        Retrieves a user from the database based on the provided data.

        Args:
            data (dict): The data used to retrieve the user.

        Returns:
            tuple: The user data as a tuple.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Login", (data['email'],))
            for result in cursor.stored_results():
                user_data = result.fetchone()
            if user_data:
                return user_data
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get_all(cls):
        """
        Retrieves all users from the database.

        Returns:
            list: A list of users.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc(
                "List_customers")
            for result in cursor.stored_results():
                users = result.fetchall()
            if users:
                return users
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, id):
        """
        Retrieves a user from the database based on the provided ID.

        Args:
            id (str): The ID of the user.

        Returns:
            tuple: The user data as a tuple.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("User_by_id", (id,))
            for result in cursor.stored_results():
                user = result.fetchone()
            if user:
                return user
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def update(self):
        """
        Updates the user in the database.

        Returns:
            bool: True if the update was successful, False otherwise.

        Raises:
            Exception: If an error occurs during the update process.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Update_user", (self.id, self.full_name, self.username, self.email,
                                            self.phone_number, SecurityService.hash_password(self.password)))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'success':
                conn.connection.commit()
                return True
            elif message == 'already_exists':
                return message
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def delete(cls, id):
        """
        Deletes a user from the database based on the provided ID.

        Args:
            id (str): The ID of the user to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.

        Raises:
            Exception: If an error occurs during the deletion process.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Delete_user", (id,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'success':
                conn.connection.commit()
                return True
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def to_dict(self):
        """
        Converts the user object to a dictionary.

        Returns:
            dict: The user data as a dictionary.
        """
        data = {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "user_type": self.user_type,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
        return {key: value for key, value in data.items() if value is not None}

from bcrypt import checkpw, gensalt, hashpw


class User():
    """
    The User class represents a user in the system, providing functionalities to manage user information and authentication.

    Attributes:
        id (str): The unique identifier of the user.
        full_name (str): The full name of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        phone_number (str): The phone number of the user.
        password (str): The hashed password of the user for authentication.
        user_type (str): The type/category of the user (e.g., admin, customer).
        created_at (datetime): The timestamp when the user account was created.
        updated_at (datetime): The timestamp of the last update to the user's information.

    Methods:
        hash_password(password): Static method that takes a plaintext password as input and returns a hashed password.
        check_password(hashed_password, password): Static method that checks if a given plaintext password matches the hashed password.
        to_dict(): Converts the User object's attributes to a dictionary for easier serialization.
    """

    def __init__(self, **kwargs):
        """
        Initializes the instance of the User class.

        Args:
            **kwargs: a dictionary of keyword arguments. The keywords must match the names of the class attributes.
        """
        self.id = kwargs.get('id')
        self.full_name = kwargs.get('full_name')
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.phone_number = kwargs.get('phone_number')
        self.password = kwargs.get('password')
        self.user_type = kwargs.get('user_type')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')

    @staticmethod
    def hash_password(password):
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    @staticmethod
    def check_password(hashed_password, password):
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def to_dict(self):
        """
        Converts the User object to a dictionary.
        """
        return {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
            "user_type": self.user_type,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }



class User():
    """
    The User class represents a user in the system.

    Attributes:
        id : The ID of the user.
        full_name : The full name of the user.
        email : The user's email address.
        password : The user's password.
        user_type : The user's type.
        created_at: The date and time the user was created.
        updated_at : The date and time of the user's last update.
    """

    def __init__(self, **kwargs):
        """
        Initializes the instance of the User class.

        Args:
            **kwargs: a dictionary of keyword arguments. The keywords must match the names of the class attributes.
        """
        self.id = kwargs.get('id')
        self.full_name = kwargs.get('full_name')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.user_type = kwargs.get('user_type')
        self.created_at = kwargs.get('created_at')
        self.updated_at = kwargs.get('updated_at')

    def to_dict(self):
        """
        Converts the User object to a dictionary.
        """
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "user_type": self.user_type,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

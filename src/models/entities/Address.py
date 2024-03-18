
class Address():
    """
    The Address class represents a physical address.

    Attributes:
        id (str): The unique identifier for the address.
        user_id (str): The unique identifier for the user associated with the address.
        state (str): The state where the address is located.
        city (str): The city where the address is located.
        address (str): The street address.

    Methods:
        to_dict(): Returns a dictionary representation of the address object.

    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.user_id = kwargs.get('user_id')
        self.state = kwargs.get('state')
        self.city = kwargs.get('city')
        self.address = kwargs.get('address')

    def to_dict(self):
        data = {
            "id": self.id,
            "user_id": self.id,
            "staet": self.state,
            "city": self.city,
            "address": self.address
        }
        return {key: value for key, value in data.items() if value is not None}

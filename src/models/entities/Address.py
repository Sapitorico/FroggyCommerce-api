
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
        self.department = kwargs.get('department')
        self.locality = kwargs.get('locality')
        self.street_address = kwargs.get('street_address')
        self.number = kwargs.get('number')
        self.type = kwargs.get('type')
        self.additional_references = kwargs.get('additional_references')
        self.created_at = kwargs.get('created_at') 
        

    def to_dict(self):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "department": self.department,
            "locality": self.locality,
            "street_address": self.street_address,
            "number": self.number,
            "type": self.type,
            "additional_references": self.additional_references
        }
        return {key: value for key, value in data.items() if value is not None}

from flask import jsonify

# Models
from src.models.AddressModel import AddressModel


class AddressController():
    """
    Controller class for managing addresses.
    """

    @classmethod
    def add_address(cls, user_id, data):
        """
        Add a new address for a user.

        Args:
            user_id (str): The ID of the user.
            data (dict): The address data.

        Returns:
            tuple: A tuple containing the JSON response and the HTTP status code.
        """
        validation = cls.validate(data)
        if validation:
            return validation
        address = AddressModel(None, user_id, data['department'], data['locality'], data['street_address'],
                               data['number'], data['type'], data['additional_references'])
        response = address.add()
        if not response:
            return jsonify({"success": False, "message": "User not found"}), 404
        return jsonify({"success": True, "message": "Address added successfully"}), 201

    @classmethod
    def get_all_addresses(cls, user_id):
        """
        Get all addresses for a user.

        Args:
            user_id (str): The ID of the user.

        Returns:
            tuple: A tuple containing the JSON response and the HTTP status code.
        """
        addresses = AddressModel.get_all(user_id)
        if not addresses:
            return jsonify({"success": False, "message": "User not found"}), 404
        addresses = [AddressModel(address[0], user_id, address[1], address[2], address[3], address[4],
                                  address[5], address[6]).to_dict() for address in addresses]
        return jsonify({"success": True, "message": "Addresses recovered successfully", "addresses": addresses}), 200

    @classmethod
    def get_address(cls, address_id):
        """
        Get an address by its ID.

        Args:
            address_id (str): The ID of the address.

        Returns:
            tuple: A tuple containing the JSON response and the HTTP status code.
        """
        address = AddressModel.get_by_id(address_id)
        if not address:
            return jsonify({"success": False, "message": "Address not found"}), 404
        address = AddressModel(address[0], None, address[1], address[2], address[3], address[4],
                               address[5], address[6]).to_dict()
        return jsonify({"success": True, "message": "Address recovered successfully", "address": address}), 200

    @classmethod
    def update_address(cls, address_id, data):
        """
        Update an address.

        Args:
            address_id (str): The ID of the address.
            data (dict): The updated address data.

        Returns:
            tuple: A tuple containing the JSON response and the HTTP status code.
        """
        validation = cls.validate(data)
        if validation:
            return validation
        address = AddressModel(address_id, None, data['department'], data['locality'], data['street_address'],
                               data['number'], data['type'], data['additional_references'])
        response = address.update()
        if not response:
            return jsonify({"success": False, "message": "Address not found"}), 404
        return jsonify({"success": True, "message": "Address updated successfully"}), 200

    @classmethod
    def delete_address(cls, address_id):
        """
        Delete an address.

        Args:
            address_id (str): The ID of the address.

        Returns:
            tuple: A tuple containing the JSON response and the HTTP status code.
        """
        response = AddressModel.delete(address_id)
        if not response:
            return jsonify({"success": False, "message": "Address not found"}), 404
        return jsonify({"success": True, "message": "Address deleted successfully"}), 200

    @staticmethod
    def validate(data):
        """
        Validate the address data.

        Args:
            data (dict): The address data.

        Returns:
            None or tuple: None if the data is valid, otherwise a tuple containing the JSON response and the HTTP status code.
        """
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        required_fields = ['department', 'locality',
                           'street_address', 'number', 'type', 'additional_references']

        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "message": f"Field '{field}' is required"}), 400
            elif field == 'type' and data[field] not in ['work', 'home']:
                return jsonify({"success": False, "message": "Field 'type' must be either 'work' or 'home'"}), 400
            elif field != 'additional_references' and (not isinstance(data[field], str) or len(data[field]) == 0):
                return jsonify({"success": False, "message": f"Field '{field}' must be a non-empty string"}), 400

        return None

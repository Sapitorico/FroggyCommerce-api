import uuid
from flask import jsonify


class ModelAddress():
    """
    The ModelAddress class provides methods for adding and validating addresses in a database.
    """

    @classmethod
    def add_address(cls, db, user_id, address):
        """
        Adds an address to the database.

        Parameters:
        - db (database connection): The connection to the database.
        - address (Address object): The address to be added.

        Returns:
        - JSON response: A JSON response indicating the success or failure of the operation.

        Raises:
        - Exception: If an error occurs during the operation.

        """
        try:
            cursor = db.cursor()
            address_id = str(uuid.uuid4())
            cursor.callproc("Add_address", (address_id, user_id,
                            address.state, address.city, address.address))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                return jsonify({"success": False, "message": "User not found"}), 404
            elif message == 'success':
                db.commit()
                return jsonify({"success": True, "message": "Address added successfully"}), 201
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @staticmethod
    def validate(data):
        """
        Validates the data for adding an address.

        Parameters:
        - data (dict): The data to be validated.

        Returns:
        - JSON response: A JSON response indicating the success or failure of the validation.

        """
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        if "state" not in data:
            return jsonify({"success": False, "message": "Field 'state' is required"}), 400
        elif not isinstance(data['state'], str) or len(data['state']) == 0:
            return jsonify({"success": False, "message": "Field 'state' must be a non-empty string"}), 400

        if "city" not in data:
            return jsonify({"success": False, "message": "Field 'city' is required"}), 400
        elif not isinstance(data['city'], str) or len(data['city']) == 0:
            return jsonify({"success": False, "message": "Field 'city' must be a non-empty string"}), 400

        if "address" not in data:
            return jsonify({"success": False, "message": "Field 'address' is required"}), 400
        elif not isinstance(data['address'], str) or len(data['address']) == 0:
            return jsonify({"success": False, "message": "Field 'address' must be a non-empty string"}), 400

        return None

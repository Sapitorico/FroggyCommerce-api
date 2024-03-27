import uuid
from flask import jsonify

# Entities
from src.models.entities.Address import Address


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
                            address.department, address.locality,
                            address.street_address, address.number,
                            address.type, address.additional_references,))
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

    @classmethod
    def list_addresses(cls, db, user_id):
        """
        Retrieves a list of addresses associated with a user from the database.

        Parameters:
        - db (database connection): The connection to the database.
        - user_id (str): The unique identifier for the user.

        Returns:
        - JSON response: A JSON response containing the list of addresses.

        Raises:
        - Exception: If an error occurs during the operation.

        """
        try:
            cursor = db.cursor()
            cursor.callproc("List_addresses", (user_id,))
            for results in cursor.stored_results():
                result = results.fetchall()
            addresses = [Address(id=address[0],
                                 department=address[1],
                                 locality=address[2],
                                 street_address=address[3],
                                 number=address[4],
                                 type=address[5],
                                 additional_references=address[6]).to_dict() for address in result]
            return jsonify({"success": True, "message": "Addresses recovered successfully", "addresses": addresses}), 200
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def get_address_by_id(cls, db, id):
        """
        Retrieves an address from the database based on its unique identifier.

        Parameters:
        - db (database connection): The connection to the database.
        - id (str): The unique identifier for the address.

        Returns:
        - JSON response: A JSON response containing the retrieved address.

        Raises:
        - Exception: If an error occurs during the operation.
        """
        try:
            cursor = db.cursor()
            cursor.callproc("Get_address", (id,))
            for result in cursor.stored_results():
                address = result.fetchone()
            if not address:
                return jsonify({"success": False, "message": "Address not found"}), 404
            address = Address(id=address[0],
                              department=address[1],
                              locality=address[2],
                              street_address=address[3],
                              number=address[4],
                              type=address[5],
                              additional_references=address[6]).to_dict()
            return jsonify({"success": True, "message": "Addres recovered successfully", "address": address}), 200
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def update_address(cls, db, id, address):
        """
        Updates an address in the database based on its unique identifier.

        Parameters:
        - db (database connection): The connection to the database.
        - id (str): The unique identifier for the address.
        - address (Address object): The updated address.

        Returns:
        - JSON response: A JSON response indicating the success or failure of the update operation.

        Raises:
        - Exception: If an error occurs during the operation.

        """
        try:
            cursor = db.cursor()
            cursor.callproc("Update_address", (id, address.department, address.locality, address.street_address,
                            address.number, address.type, address.additional_references,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                return jsonify({"success": False, "message": "Address not found"}), 404
            elif message == 'success':
                db.commit()
                return jsonify({"success": True, "message": "Address updated successfully"}), 200
        except Exception as e:
            return jsonify({"success": False, "Error": str(e)}), 500
        finally:
            cursor.close()

    @classmethod
    def delete_address(cls, db, id):
        """
        Deletes an address from the database based on its unique identifier.

        Parameters:
        - db (database connection): The connection to the database.
        - id (str): The unique identifier for the address.

        Returns:
        - JSON response: A JSON response indicating the success or failure of the delete operation.

        Raises:
        - Exception: If an error occurs during the operation.

        """
        try:
            cursor = db.cursor()
            cursor.callproc("Delete_address", (id,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'not_exist':
                return jsonify({"success": False, "message": "Address not found"}), 404
            elif message == 'success':
                db.commit()
                return jsonify({"success": True, "message": "Address deleted successfully"}), 200
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

import uuid

# Data Base servie
from src.services.DataBaseService import DataBaseService

conn = DataBaseService()


class AddressModel():
    """
    Represents an address model.
    """

    def __init__(self, id, user_id, department, locality, street_address, number, type,
                 additional_references, created_at=None, updated_at=None):
        """
        Initializes a new instance of the AddressModel class.

        Args:
            id (str): The unique identifier of the address.
            user_id (str): The user ID associated with the address.
            department (str): The department of the address.
            locality (str): The locality of the address.
            street_address (str): The street address of the address.
            number (str): The number of the address.
            type (str): The type of the address.
            additional_references (str): Additional references for the address.
            created_at (datetime, optional): The timestamp when the address was created.
            updated_at (datetime, optional): The timestamp when the address was last updated.
        """
        self.id = id if id is not None else str(uuid.uuid4())
        self.user_id = user_id
        self.department = department
        self.locality = locality
        self.street_address = street_address
        self.number = number
        self.type = type
        self.additional_references = additional_references
        self.created_at = created_at
        self.updated_at = updated_at

    def add(self):
        """
        Adds the address to the database.

        Returns:
            bool: True if the address was successfully added, False otherwise.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Add_address", (self.id, self.user_id, self.department, self.locality,
                                            self.street_address, self.number, self.type, self.additional_references,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'success':
                conn.connection.commit()
                return True
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get_all(cls, user_id):
        """
        Retrieves all addresses for a given user.

        Args:
            user_id (str): The user ID.

        Returns:
            list: A list of addresses for the user.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("List_addresses", (user_id,))
            for results in cursor.stored_results():
                addresses = results.fetchall()
            if addresses:
                return addresses
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, id):
        """
        Retrieves an address by its ID.

        Args:
            id (str): The ID of the address.

        Returns:
            tuple: The address information.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Get_address", (id,))
            for result in cursor.stored_results():
                address = result.fetchone()
            if address:
                return address
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def update(self):
        """
        Updates the address in the database.

        Returns:
            bool: True if the address was successfully updated, False otherwise.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Update_address", (self.id, self.department, self.locality, self.street_address,
                            self.number, self.type, self.additional_references,))
            for result in cursor.stored_results():
                message = result.fetchone()[0]
            if message == 'success':
                conn.connection.commit()
                return True
        except Exception as e:
            print(e)
        finally:
            conn.close()

    @classmethod
    def delete(cls, id):
        """
        Deletes an address from the database.

        Args:
            id (str): The ID of the address to delete.

        Returns:
            bool: True if the address was successfully deleted, False otherwise.
        """
        try:
            cursor = conn.get_cursor()
            cursor.callproc("Delete_address", (id,))
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
        Converts the address object to a dictionary.

        Returns:
            dict: The address information as a dictionary.
        """
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "department": self.department,
            "locality": self.locality,
            "street_address": self.street_address,
            "number": self.number,
            "type": self.type,
            "additional_references": self.additional_references,
        }
        return {key: value for key, value in data.items() if value is not None}

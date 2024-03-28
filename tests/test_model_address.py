import unittest

# Entities
from src.models.entities.Address import Address
from src.models.entities.Users import User

# BaseTestContext
from . import BaseTestContext

# Models
from src.models.ModelAddress import ModelAddress
from src.models.ModelUser import ModelUser


class TestModelAddress(BaseTestContext):

    def register_user(self):
        user = User(full_name="Sapito Rico",
                    username="sapitorico",
                    email="example@gmail.com",
                    phone_number="12345678",
                    password=User.hash_password("12345678"))
        ModelUser.register(self.connection, user)
        data = User(email="example@gmail.com",
                    password="12345678")
        response = ModelUser.login(self.connection, data)
        return response[0].json['user']['id']

    def add_address(self, user_id):
        address = Address(department="departament",
                          locality="locality",
                          street_address="street_address",
                          number="number",
                          type="home",
                          additional_references="additional_references")
        ModelAddress.add_address(self.connection, user_id, address)

    def test_validate(self):
        data = {}
        response = ModelAddress.validate(data)
        self.assertEqual(response[1], 400)
        self.assertEqual(
            response[0].json, {"success": False, "message": "No data provided"})

        data = {"department": "department"}
        response = ModelAddress.validate(data)
        self.assertEqual(response[1], 400)
        self.assertEqual(
            response[0].json, {"success": False, "message": "Field 'locality' is required"})

        data = {"department": "department", "locality": "locality"}
        response = ModelAddress.validate(data)
        self.assertEqual(response[1], 400)
        self.assertEqual(
            response[0].json, {"success": False, "message": "Field 'street_address' is required"})

        data = {"department": "department", "locality": "locality",
                "street_address": "street_address", "number": "number", "type": "home", "additional_references": "additional_references"}
        response = ModelAddress.validate(data)
        self.assertEqual(response, None)

    def test_add_address(self):
        user_id = self.register_user()
        address = Address(department="department",
                          locality="locality",
                          street_address="street_address",
                          number="number",
                          type="home",
                          additional_references="additional_references")
        response = ModelAddress.add_address(self.connection, user_id, address)
        self.assertEqual(response[1], 201)
        self.assertEqual(response[0].json, {
                         "success": True, "message": "Address added successfully"})

    def test_add_address_invalid_user(self):
        address = Address(department="department",
                          locality="locality",
                          street_address="street_address",
                          number="number",
                          type="home",
                          additional_references="additional_references")
        response = ModelAddress.add_address(self.connection, 1, address)
        self.assertEqual(response[1], 404)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "User not found"})

    def test_list_addresses(self):
        user_id = self.register_user()
        self.add_address(user_id)
        response = ModelAddress.list_addresses(self.connection, user_id)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].json['success'], True)

    def test_get_address_by_id(self):
        user_id = self.register_user()
        self.add_address(user_id)
        response = ModelAddress.list_addresses(self.connection, user_id)
        address_id = response[0].json['addresses'][0]['id']
        response = ModelAddress.get_address_by_id(self.connection, address_id)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].json['success'], True)

    def test_update_address(self):
        user_id = self.register_user()
        self.add_address(user_id)
        response = ModelAddress.list_addresses(self.connection, user_id)
        address_id = response[0].json['addresses'][0]['id']
        address = Address(department="department",
                          locality="locality",
                          street_address="street_address",
                          number="number",
                          type="home",
                          additional_references="additional_references")
        response = ModelAddress.update_address(
            self.connection, address_id, address)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].json, {
                         "success": True, "message": "Address updated successfully"})

    def test_delete_address(self):
        user_id = self.register_user()
        self.add_address(user_id)
        response = ModelAddress.list_addresses(self.connection, user_id)
        address_id = response[0].json['addresses'][0]['id']
        response = ModelAddress.delete_address(self.connection, address_id)
        self.assertEqual(response[1], 200)
        self.assertEqual(response[0].json, {
                         "success": True, "message": "Address deleted successfully"})


if __name__ == '__main__':
    unittest.main()

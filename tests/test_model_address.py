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
        address = Address(state="state",
                          city="city",
                          address="address")
        ModelAddress.add_address(self.connection, user_id, address)

    def test_validate(self):
        data = {}
        response = ModelAddress.validate(data)
        self.assertEqual(response[1], 400)
        self.assertEqual(
            response[0].json, {"success": False, "message": "No data provided"})

        data = {"state": "state"}
        response = ModelAddress.validate(data)
        self.assertEqual(response[1], 400)
        self.assertEqual(
            response[0].json, {"success": False, "message": "Field 'city' is required"})

        data = {"state": "state", "city": "city"}
        response = ModelAddress.validate(data)
        self.assertEqual(response[1], 400)
        self.assertEqual(
            response[0].json, {"success": False, "message": "Field 'address' is required"})

        data = {"state": "state", "city": "city", "address": "address"}
        response = ModelAddress.validate(data)
        self.assertEqual(response, None)

    def test_add_address(self):
        user_id = self.register_user()
        address = Address(state="state",
                          city="city",
                          address="address")
        response = ModelAddress.add_address(self.connection, user_id, address)
        self.assertEqual(response[1], 201)
        self.assertEqual(response[0].json, {
                         "success": True, "message": "Address added successfully"})

    def test_add_address_invalid_user(self):
        address = Address(state="state",
                          city="city",
                          address="address")
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


if __name__ == '__main__':
    unittest.main()

import unittest

# Entities
from src.models.entities.Users import User

# BaseTestContext
from . import BaseTestContext

# Models
from src.models.ModelUser import ModelUser


class TestModelUser(BaseTestContext):

    def register_user(self):
        user = User(full_name="Sapito Rico",
                    username="sapitorico",
                    email="example@gmail.com",
                    phone_number="1234567890",
                    password=User.hash_password("12345678"))
        ModelUser.register(self.connection, user)

    def test_valid_data(self):
        data = {
            "full_name": "John Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "password": "password123"
        }

        result = ModelUser.validate(data)
        self.assertIsNone(result)

    def test_empty_data(self):
        data = {}

        result = ModelUser.validate(data)
        self.assertEqual(result[0].json, {
                         "success": False, "message": "No data provided"})
        self.assertEqual(result[1], 400)

    def test_invalid_username(self):
        data = {
            "full_name": "Sapito Rico",
            "username": "",
            "email": "emailexample@gmail.com",
            "phone_number": "1234567890",
            "password": "12345678"
        }
        result = ModelUser.validate(data)
        self.assertEqual(result[0].json, {
            "success": False, "message": "Field 'username' must be a non-empty string"})
        self.assertEqual(result[1], 400)

    def test_invalid_email(self):
        data = {
            "full_name": "Sapito Rico",
            "username": "sapitorico",
            "email": "emailexample.com",
            "phone_number": "1234567890",
            "password": "12345678"
        }

        result = ModelUser.validate(data)
        self.assertEqual(result[0].json, {
                         "success": False, "message": "Invalid email format"})
        self.assertEqual(result[1], 400)

    def test_invalid_phone_number(self):
        data = {
            "full_name": "Sapito Rico",
            "username": "sapitorico",
            "email": "emailexample@gmail.com",
            "phone_number": "12345abc",
            "password": "12345678"
        }
        result = ModelUser.validate(data)
        self.assertEqual(result[0].json, {
            "success": False, "message": "Invalid phone number format"})
        self.assertEqual(result[1], 400)

    def test_invalid_password(self):
        data = {
            "full_name": "Sapito RIco",
            "username": "sapitorico",
            "email": "emailexample@gmail.com",
            "phone_number": "1234567890",
            "password": "123"
        }
        result = ModelUser.validate(data)
        self.assertEqual(result[0].json, {
            "success": False, "message": "Password must be at least 8 characters long"})
        self.assertEqual(result[1], 400)

    def test_invalid_full_name(self):
        data = {
            "full_name": "Sapito",
            "username": "sapitorico",
            "email": "emailexample@gmail.com",
            "phone_number": "1234567890",
            "password": "12345678"
        }
        result = ModelUser.validate(data)
        self.assertEqual(result[0].json, {
                         "success": False, "message": "Full name field must contain both first and last name"})
        self.assertEqual(result[1], 400)

    def test_success_register(self):
        user = User(full_name="Sapito Rico",
                    username="sapitorico",
                    email="example@gmail.com",
                    phone_number="1234567890",
                    password=User.hash_password("12345678"))
        response = ModelUser.register(self.connection, user)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json, {
                         'message': "User 'Sapito Rico' successfully registered", 'success': True})
        self.assertEqual(response[1], 201)

    def test_already_registered(self):
        user = User(full_name="Sapito Rico",
                    username="sapitorico",
                    email="example@gmail.com",
                    phone_number="1234567890",
                    password=User.hash_password("12345678"))
        ModelUser.register(self.connection, user)
        response = ModelUser.register(self.connection, user)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "This 'user' is already registered"})
        self.assertEqual(response[1], 400)

    def test_login_success(self):
        self.register_user()
        data = User(email="example@gmail.com",
                    password="12345678")
        response = ModelUser.login(self.connection, data)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json['message'],
                         "Successful login, welcome 'Sapito Rico'")
        self.assertEqual(response[0].json['success'], True)
        self.assertEqual(response[0].json['user']['full_name'], "Sapito Rico")
        self.assertEqual(response[0].json['user']['username'], "sapitorico")
        self.assertEqual(response[0].json['user']
                         ['email'], "example@gmail.com")
        self.assertEqual(response[0].json['user']
                         ['phone_number'], "1234567890")
        self.assertEqual(response[0].json['user']['user_type'], "customer")
        self.assertEqual(response[1], 200)
        self.assertIn('id', response[0].json['user'])
        self.assertIn('token', response[0].json)
        self.assertIn('created_at', response[0].json['user'])
        self.assertIn('updated_at', response[0].json['user'])

    def test_login_fail(self):
        data = User(email="example@gmail.com",
                    password="12345678")
        response = ModelUser.login(self.connection, data)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "Incorrect credentials"})
        self.assertEqual(response[1], 400)

    def test_login_invalid_password(self):
        self.register_user()
        data = User(email="example@gmail.com",
                    password="12345679")
        response = ModelUser.login(self.connection, data)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "Incorrect credentials"})
        self.assertEqual(response[1], 400)

    def test_get_users(self):
        self.register_user()
        response = ModelUser.get_users(self.connection)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json['message'],
                         "Users fetched successfully")
        self.assertEqual(response[0].json['success'], True)
        self.assertEqual(response[0].json['users'][0]
                         ['email'], "example@gmail.com")
        self.assertEqual(response[0].json['users'][0]
                         ['full_name'], "Sapito Rico")
        self.assertEqual(response[0].json['users'][0]['user_type'], "customer")
        self.assertEqual(response[1], 200)
        self.assertIn('id', response[0].json['users'][0])
        self.assertIn('created_at', response[0].json['users'][0])
        self.assertIn('updated_at', response[0].json['users'][0])

    def test_get_user_by_id(self):
        self.register_user()
        data = User(email="example@gmail.com",
                    password="12345678")
        res = ModelUser.login(self.connection, data)
        id = res[0].json['user']['id']
        response = ModelUser.get_user_by_id(self.connection, id)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json['message'],
                         "User fetched successfully")
        self.assertEqual(response[0].json['success'], res[0].json['success'])
        self.assertEqual(response[0].json['user']
                         ['email'], res[0].json['user']['email'])
        self.assertEqual(response[0].json['user']
                         ['phone_number'], res[0].json['user']['phone_number'])
        self.assertEqual(response[0].json['user']
                         ['username'], res[0].json['user']['username'])
        self.assertEqual(response[0].json['user']
                         ['full_name'], res[0].json['user']['full_name'])
        self.assertEqual(response[0].json['user']['user_type'],
                         response[0].json['user']['user_type'])
        self.assertEqual(
            response[0].json['user']['created_at'], res[0].json['user']['created_at'])
        self.assertEqual(
            response[0].json['user']['updated_at'], res[0].json['user']['created_at'])
        self.assertEqual(id, response[0].json['user']['id'])
        self.assertEqual(response[1], 200)

    def test_get_user_by_id_fail(self):
        response = ModelUser.get_user_by_id(self.connection, 1)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "User not found"})
        self.assertEqual(response[1], 404)

    def test_update_user(self):
        self.register_user()
        data = User(email="example@gmail.com",
                    password="12345678")
        res = ModelUser.login(self.connection, data)
        id = res[0].json['user']['id']
        response = ModelUser.update_user(
            self.connection, id, {"full_name": res[0].json['user']['full_name'], "email": "update@gmail.com", "password": "87654321"})
        updated_user = ModelUser.get_user_by_id(self.connection, id)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json['message'],
                         "User successfully updated")
        self.assertTrue(response[0].json['success'])
        self.assertEqual(response[1], 200)
        self.assertEqual(updated_user[0].json['user']
                         ['email'], "update@gmail.com")
        self.assertEqual(
            updated_user[0].json['user']['full_name'], res[0].json['user']['full_name'])

    def test_update_user_fail(self):
        response = ModelUser.update_user(
            self.connection, 1, {"full_name": "Sapito Rico", "email": "update@gmail.com", "password": "87654321"})
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "User not found"})
        self.assertEqual(response[1], 404)

    def test_delete_user(self):
        self.register_user()
        data = User(email="example@gmail.com",
                    password="12345678")
        res = ModelUser.login(self.connection, data)
        id = res[0].json['user']['id']
        response = ModelUser.delete_user(self.connection, id)
        user = ModelUser.get_user_by_id(self.connection, id)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json, {
                         "success": True, "message": "User successfully deleted"})
        self.assertEqual(response[1], 200)
        self.assertEqual(
            user[0].json, {"success": False, "message": "User not found"})

    def test_delete_user_fail(self):
        response = ModelUser.delete_user(self.connection, 1)
        self.assertIsInstance(response, tuple)
        self.assertEqual(response[0].json, {
                         "success": False, "message": "User not found"})
        self.assertEqual(response[1], 404)


if __name__ == "__main__":
    unittest.main()

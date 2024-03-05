import unittest

from src.models.entities.Users import User

from . import BaseTestContext

# Models
from src.models.ModelUser import ModelUser


class TestValidDateModelUser(BaseTestContext):

    def register_user(self):
        user = User(full_name="Sapito Rico",
                    email="example@gmail.com",
                    password=User.hash_password("12345678"),
                    user_type='customer')
        ModelUser.register(self.connection, user)

    # def test_valid_data(self):
    #     data = {
    #         "full_name": "John Doe",
    #         "email": "johndoe@example.com",
    #         "password": "password123"
    #     }

    #     result = ModelUser.validate(data)
    #     self.assertIsNone(result)

    # def test_empty_data(self):
    #     data = {}

    #     result = ModelUser.validate(data)
    #     self.assertEqual(result[0].json, {
    #                      "success": False, "message": "No data provided"})
    #     self.assertEqual(result[1], 400)

    # def test_invalid_email(self):
    #     data = {
    #         "full_name": "Sapito Rico",
    #         "email": "emailexample.com",
    #         "password": "12345678"
    #     }

    #     result = ModelUser.validate(data)
    #     self.assertEqual(result[0].json, {
    #                      "success": False, "message": "Invalid email format"})
    #     self.assertEqual(result[1], 400)

    # def test_invalid_password(self):
    #     data = {
    #         "full_name": "Sapito RIco",
    #         "email": "emailexample@gmail.com",
    #         "password": "123"
    #     }
    #     result = ModelUser.validate(data)
    #     self.assertEqual(result[0].json, {
    #         "success": False, "message": "Password must be at least 8 characters long"})
    #     self.assertEqual(result[1], 400)

    # def test_invalid_full_name(self):
    #     data = {
    #         "full_name": "Sapito",
    #         "email": "emailexample@gmail.com",
    #         "password": "12345678"
    #     }
    #     result = ModelUser.validate(data)
    #     self.assertEqual(result[0].json, {
    #                      "success": False, "message": "Full name field must contain both first and last name"})
    #     self.assertEqual(result[1], 400)

    # def test_success_register(self):
    #     user = User(full_name="Sapito Rico",
    #                 emal="example@gmail.com",
    #                 password=User.hash_password("12345678"))
    #     response = ModelUser.register(self.connection, user)
    #     self.assertEqual(response[0].json, {
    #                      'message': "User 'Sapito Rico' successfully registered", 'success': True})
    #     self.assertEqual(response[1], 201)

    def test_already_registered(self):
        user = User(full_name="Sapito Rico",
                    email="example@gmail.com",
                    password=User.hash_password("12345678"),
                    user_type='customer')
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
        self.assertEqual(response[0].json['user']
                         ['email'], "example@gmail.com")
        self.assertEqual(response[0].json['user']['full_name'], "Sapito Rico")
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

if __name__ == "__main__":
    unittest.main()

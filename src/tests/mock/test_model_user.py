import unittest
from datetime import datetime
from unittest.mock import MagicMock
from src.models.ModelUser import ModelUser
from src.models.entities.Users import User
from flask import Flask


class TestModelUser(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.db = MagicMock()

    def tearDown(self):
        self.app_context.pop()

    def test_login_correct_credentials(self):
        mock_cursor = MagicMock()
        hashed_password = User.hash_password("password")
        created_at = datetime.strptime(
            "2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        mock_cursor.fetchone.return_value = (
            1, "John Doe", "john@example.com", hashed_password, "customer", created_at)
        self.db.cursor.return_value = mock_cursor

        user = User(email="john@example.com", password="password")

        response = ModelUser.login(self.db, user)

        self.assertTrue(response[0].json["success"])
        self.assertEqual(response[0].json["message"],
                         "Inicio de sesión exitoso.")
        self.assertIn("token", response[0].json)
        self.assertEqual(response[0].json["user"]["id"], 1)
        self.assertEqual(response[0].json["user"]["full_name"], "John Doe")
        self.assertEqual(response[0].json["user"]["email"], "john@example.com")
        self.assertEqual(response[0].json["user"]["user_type"], "customer")
        self.assertEqual(response[0].json["user"]
                         ["created_at"], "2022-01-01 12:00:00")

    def test_login_incorrect_credentials(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        self.db.cursor.return_value = mock_cursor

        user = User(email="john@example.com", password="password")

        response = ModelUser.login(self.db, user)

        self.assertFalse(response[0].json["success"])
        self.assertEqual(response[0].json["message"],
                         "Credenciales incorrectas.")

    def test_login_user_not_found(self):
        mock_cursor = MagicMock()
        hashed_password = User.hash_password("password")
        created_at = datetime.strptime(
            "2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        mock_cursor.fetchone.return_value = (
            1, "John Doe", "john@example.com", hashed_password, "customer", created_at)
        self.db.cursor.return_value = mock_cursor

        user = User(email="", password="")

        response = ModelUser.login(self.db, user)

        self.assertFalse(response[0].json["success"])
        self.assertEqual(response[0].json["message"],
                         "Credenciales incorrectas.")

    def test_login_user_not_email(self):
        mock_cursor = MagicMock()
        hashed_password = User.hash_password("password")
        created_at = datetime.strptime(
            "2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        mock_cursor.fetchone.return_value = (
            1, "John Doe", "john@example.com", hashed_password, "customer", created_at)
        self.db.cursor.return_value = mock_cursor

        user = User(email="", password="12345678")

        response = ModelUser.login(self.db, user)

        self.assertFalse(response[0].json["success"])
        self.assertEqual(response[0].json["message"],
                         "Credenciales incorrectas.")

    def test_register_user(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        self.db.cursor.return_value = mock_cursor
        full_name = "John Doe"
        user = User(full_name=full_name,
                    email="john@example.com", password="12345678")

        response = ModelUser.register(self.db, user)

        self.assertTrue(response[0].json["success"])
        self.assertEqual(response[0].json["message"],
                         f"Usuario {full_name} registrado con éxito.")

    def test_register_user_already_exists(self):
        mock_cursor = MagicMock()
        hashed_password = User.hash_password("password")
        created_at = datetime.strptime(
            "2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        mock_cursor.fetchone.return_value = (
            1, "John Doe", "john@example.com", hashed_password, "customer", created_at)
        self.db.cursor.return_value = mock_cursor
        full_name = "John Doe"
        user = User(full_name=full_name,
                    email="john@example.com", password="12345678")

        response = ModelUser.register(self.db, user)

        self.assertFalse(response[0].json["success"])
        self.assertEqual(response[0].json["message"], "El usuario ya existe.")


if __name__ == '__main__':
    unittest.main()

# import unittest
# from src import init_app
# from src.models.entities.Users import User
# import json

# class TestLoginEndpoint(unittest.TestCase):

#     def setUp(self):
#         self.app = init_app('testing')
#         self.client = self.app.test_client()

#     def tearDown(self):
#         pass

#     def test_login_correct_credentials(self):
#         # Simulamos una solicitud POST al endpoint de login
#         response = self.client.post('/api/auth/login', json={'email': 'john@example.com', 'password': 'password'})

#         # Verificamos que la respuesta sea exitosa (código 200)
#         self.assertEqual(response.status_code, 200)

#         # Verificamos que la respuesta contenga los datos esperados
#         response_data = json.loads(response.data)
#         self.assertTrue(response_data["success"])
#         self.assertIn("token", response_data)
#         self.assertEqual(response_data["message"], "Inicio de sesión exitoso.")

# if __name__ == '__main__':
#     unittest.main()

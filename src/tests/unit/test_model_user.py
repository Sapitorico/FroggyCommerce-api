import unittest
from flask import Flask

# Models
from src.models.ModelUser import ModelUser


class TestModelUser(unittest.TestCase):

    def setUp(self):
        # Crear una aplicación Flask mínima para las pruebas
        self.app = Flask(__name__)
        # Activar el contexto de la aplicación Flask
        self.app_context = self.app.test_request_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_validate_data_register(self):
        validation_cases = [
            {
                "data": {
                    "full_name": "John Doe",
                    "email": "john@example.com",
                    "password": "12345678",
                },
                "expected_error": None,
            },
            {
                "data": {
                    "full_name": "John Doe",
                },
                "expected_error": "Faltan los siguientes campos: email, password.",
            },
            {
                "data": {
                    "email": "john@example.com",
                },
                "expected_error": "Faltan los siguientes campos: full_name, password.",
            },
            {
                "data": {
                    "password": "12345678",
                },
                "expected_error": "Faltan los siguientes campos: full_name, email.",
            },
            {
                "data": {
                },
                "expected_error": "No se proporcionaron datos.",
            },
            {
                "data": {
                    "full_name": "John",
                    "email": "john@example.com",
                    "password": "12345678",
                },
                "expected_error": "El nombre completo debe contener al menos nombre y apellido.",
            },
            {
                "data": {
                    "full_name": "John Doe",
                    "email": "johnexample.com",
                    "password": "12345678",
                },
                "expected_error": "Formato de correo electrónico inválido.",
            },
            {
                "data": {
                    "full_name": "John Doe",
                    "email": "john@example.com",
                    "password": "1234567",
                },
                "expected_error": "La contraseña debe tener al menos 8 caracteres.",
            },
        ]
        for i, case in enumerate(validation_cases):
            with self.subTest(test_case_number=i):
                with self.app.test_request_context():
                    response = ModelUser.validate_data_register(case["data"])
                    if case["expected_error"] is None:
                        self.assertIsNone(
                            response,
                            "Se esperaba una respuesta None para datos válidos",
                        )
                    else:
                        self.assertIsNotNone(
                            response, "Se esperaba una respuesta de error"
                        )
                        self.assertEqual(
                            response[0].json["message"],
                            case["expected_error"],
                            "Mensaje de error incorrecto",
                        )

    def test_validate_data_login(self):
        validation_cases = [
            {
                "data": {
                    "email": "john@example.com",
                    "password": "12345678",
                },
                "expected_error": None,
            },
            {
                "data": {
                    "email": "john@example.com",
                },
                "expected_error": "Faltan los siguientes campos: password.",
            },
            {
                "data": {
                    "password": "12345678",
                },
                "expected_error": "Faltan los siguientes campos: email.",
            },
            {
                "data": {
                },
                "expected_error": "No se proporcionaron datos.",
            },
            {
                "data": {
                    "email": "johnexample.com",
                    "password": "12345678",
                },
                "expected_error": "Formato de correo electrónico inválido.",
            },
            {
                "data": {
                    "email": "john@example.com",
                    "password": "1234567",
                },
                "expected_error": "La contraseña debe tener al menos 8 caracteres.",
            },
        ]
        for i, case in enumerate(validation_cases):
            with self.subTest(test_case_number=i):
                with self.app.test_request_context():
                    response = ModelUser.validate_data_login(case["data"])
                    if case["expected_error"] is None:
                        self.assertIsNone(
                            response,
                            "Se esperaba una respuesta None para datos válidos",
                        )
                    else:
                        self.assertIsNotNone(
                            response, "Se esperaba una respuesta de error"
                        )
                        self.assertEqual(
                            response[0].json["message"],
                            case["expected_error"],
                            "Mensaje de error incorrecto",
                        )


if __name__ == "__main__":
    unittest.main()

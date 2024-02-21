import re
from bcrypt import checkpw, gensalt, hashpw
from flask import jsonify


class User():

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.full_name = kwargs.get('full_name')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.user_type = kwargs.get('user_type')
        self.created_at = kwargs.get('created_at')

    @staticmethod
    def hash_password(password):
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    @staticmethod
    def check_password(hashed_password, password):
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"success": False, "message": "Formato de correo electrónico inválido"}), 400
        return None

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return jsonify({"success": False, "message": "La contraseña debe tener por lo menos 8 caracteres"}), 400
        return None

    @staticmethod
    def validate_full_name(full_name):
        if len(full_name.split(' ')) < 2:
            return jsonify({"success": False, "message": "El campo full_name debe contener un nombre y apellido"}), 400
        return None

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "user_type": self.user_type,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

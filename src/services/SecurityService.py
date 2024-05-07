from functools import wraps
import jwt
import pytz
from os import getenv
from datetime import datetime, timedelta
from flask import jsonify, request
from bcrypt import checkpw, gensalt, hashpw


class SecurityService():
    # Get the secret key from environment variables
    _secret = getenv('JWT_SECRET')
    _algorithm = getenv('ALGORITHM')
    _tz = pytz.timezone('America/Montevideo')

    @staticmethod
    def hash_password(password):
        """
        Hashes the given password using bcrypt algorithm.
        """
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    @staticmethod
    def check_password(hashed_password, password):
        """
        Checks if the given password matches the hashed password.
        """
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @classmethod
    def generate_token(cls, user):
        """
        Generate a JWT token based on the user information.

        Returns:
            str: Generated JWT token.
        """
        payload = {
            "iat": datetime.now(tz=cls._tz),  # Token issuance date and time
            "exp": datetime.now(tz=cls._tz) + timedelta(days=1),
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type,
        }
        token = jwt.encode(payload, cls._secret, algorithm=cls._algorithm)
        return token

    @classmethod
    def verify_token(cls, headers):
        """
        Verify the validity of the JWT token in the request headers.

        Returns:
            dict or tuple: Decoded token payload if valid, otherwise a tuple with an error message.
        """
        if 'Authorization' not in headers:
            return jsonify({"success": False, "message": "Unauthorized"}), 401
        authorization = headers['Authorization']
        try:
            encode_token = authorization.split(' ')[1]
            payload = jwt.decode(
                encode_token, cls._secret, algorithms=[cls._algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid token"}), 403

    @classmethod
    def verify_admin(cls, func):
        """
        Decorator to verify if the user is an administrator before executing the function.

        Returns:
            function: Decorated function.
        """
        @wraps(func)
        def decorated_function(*args, **kwargs):
            headers = request.headers
            payload = cls.verify_token(headers)
            if isinstance(payload, tuple):
                return payload
            if payload.get('user_type') == "admin":
                return func(*args, **kwargs)
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        return decorated_function

    @classmethod
    def verify_session(cls, func):
        """
        Decorator to verify if a valid user session exists before executing the function.

        Returns:
            function: Decorated function.
        """
        @wraps(func)
        def decorated_function(*args, **kwargs):
            headers = request.headers
            payload = cls.verify_token(headers)
            if isinstance(payload, tuple):
                return payload
            user_id = payload.get('id')
            if user_id:
                return func(user_id, *args, **kwargs)
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        return decorated_function

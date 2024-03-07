from functools import wraps
import jwt
import pytz
from os import getenv
from datetime import datetime, timedelta
from flask import jsonify, request


class Security():
    """
    Provides functionalities related to user authentication and authorization using JSON Web Tokens (JWT) within a Flask application.
    """

    # Get the secret key from environment variables
    secret = getenv('JWT_SECRET')
    algorithm = 'HS256'  # Encryption algorithm used
    tz = pytz.timezone('America/Montevideo')

    @classmethod
    def generate_token(cls, user):
        """
        Generate a JWT token based on the user information.

        Returns:
            str: Generated JWT token.
        """
        payload = {
            "iat": datetime.now(tz=cls.tz),  # Token issuance date and time

            # Token expiration date (1 day)
            "exp": datetime.now(tz=cls.tz) + timedelta(days=1),
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "user_type": user.user_type,
        }
        token = jwt.encode(payload, cls.secret, algorithm=cls.algorithm)
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
                encode_token, cls.secret, algorithms=[cls.algorithm])
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

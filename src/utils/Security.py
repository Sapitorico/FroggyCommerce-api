import jwt
import pytz
from os import getenv
from datetime import datetime, timedelta
from flask import jsonify


class Security():

    secret = getenv('JWT_SECRET')
    algorithm = 'HS256'
    tz = pytz.timezone('America/Montevideo')

    @classmethod
    def generate_token(cls, user):
        payload = {
            "iat": datetime.now(tz=cls.tz),
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
    def verify_admin(cls, headers):
        payload = cls.verify_token(headers)
        if isinstance(payload, tuple):
            return payload
        if payload.get('user_type') == "admin":
            return None
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    @classmethod
    def verify_session(cls, headers):
        payload = cls.verify_token(headers)
        if isinstance(payload, tuple):
            return payload
        if payload.get('id'):
            return payload.get('id')
        return jsonify({"success": False, "message": "Unauthorized"}), 403

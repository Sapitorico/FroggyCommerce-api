import jwt
import pytz
from os import getenv
from datetime import datetime, timedelta
from flask import jsonify


class Security():

    secret = getenv('JWT_SECRET')
    tz = pytz.timezone('America/Montevideo')

    @classmethod
    def getnerate_token(cls, user):
        payload = {
            "iat": datetime.now(tz=cls.tz),
            "exp": datetime.now(tz=cls.tz) + timedelta(days=1),
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "user_type": user.user_type,
        }
        token = jwt.encode(payload, cls.secret, algorithm='HS256')
        return token

    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' not in headers:
            return jsonify({"success": False, "message": "Unauthorized"}), 401
        authorization = headers['Authorization']
        try:
            encode_token = authorization.split(' ')[1]
            playload = jwt.decode(
                encode_token, cls.secret, algorithms=['HS256'])
            if playload.get('user_type') == "admin":
                return None
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"success": False, "message": "Token expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"success": False, "message": "Invalid token"}), 403

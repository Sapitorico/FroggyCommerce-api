import datetime
import jwt
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

class Security():
    
    secret = os.getenv('JWT_SECRET')
    tz = pytz.timezone('America/Montevideo')
    
    @classmethod
    def getnerate_token(cls, user):
        payload = {
            "iat": datetime.datetime.now(tz=cls.tz),
            "exp": datetime.datetime.now(tz=cls.tz) + datetime.timedelta(days=1),
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "user_type": user.user_type,
        }
        token = jwt.encode(payload, cls.secret, algorithm='HS256')
        return token
    
    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encode_token = authorization.split(' ')[1]
            try:
                playload = jwt.decode(encode_token, cls.secret, algorithms=['HS256'])
                if playload['user_type'] == "admin":
                    return True
                return False
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                return False
            
        return False
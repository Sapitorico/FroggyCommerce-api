from bcrypt import checkpw, gensalt, hashpw


class User():
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.full_name = kwargs.get('full_name')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.user_type = kwargs.get('user_type')
        self.created_at = kwargs.get('created_at')
        
    @classmethod
    def hash_password(self, password):
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
    
    @classmethod
    def check_password(self, hashed_password, password):
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "user_type": self.user_type,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
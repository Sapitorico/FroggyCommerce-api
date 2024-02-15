from bcrypt import checkpw, gensalt, hashpw


class User():
    
    def __init__(self, id, full_name, email, password, user_type, created_at):
        self.id = id
        self.full_namename = full_name
        self.email = email
        self.password = password
        self.user_type = user_type
        self.created_at = created_at
        
    @classmethod
    def check_password(self, hashed_password, password):
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

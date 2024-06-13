# Models
from src.models.UsersModel import UsersModel

# Security
from src.services.SecurityService import SecurityService


class UsersController():

    @classmethod
    def register(cls, data):
        """
        Register a new user.
        """
        user = UsersModel(full_name=data['full_name'], username=data['username'],
                          email=data['email'], phone_number=data['phone_number'], password=data['password'])
        full_name, response = user.create()
        return full_name, response

    @classmethod
    def login(cls, data):
        """
        Logs in a user with the provided credentials.
        """
        user, response = UsersModel.get(data['email'])
        if user:
            user = UsersModel(id=user[0], full_name=user[1], username=user[2], email=user[3], phone_number=user[4],
                              password=SecurityService.check_password(user[5], data['password']), user_type=user[6],
                              created_at=user[7], updated_at=user[8])
            if user.password == False:
                return None, 'not_found'
        return user, response

    @classmethod
    def get_users(cls, page, per_page, name):
        """
        Retrieve a list of users from the UsersModel.
        """
        users, total_pages, response = UsersModel.get_all(page, per_page, name)
        if users:
            users = [UsersModel(id=user[0], full_name=user[1], username=user[2], email=user[3], phone_number=user[4],
                                user_type=user[5], created_at=user[6], updated_at=user[7]).to_dict() for user in users]
        return users, total_pages, response

    @classmethod
    def get_user_by_id(cls, id):
        """
        Retrieves a user by their ID.
        """
        user, response = UsersModel.get_by_id(id)
        if user:
            user = UsersModel(id=user[0], full_name=user[1], username=user[2], email=user[3], phone_number=user[4],
                              user_type=user[5], created_at=user[6], updated_at=user[7]).to_dict()
        return user, response

    @classmethod
    def update_user(cls, id, data):
        """
        Update a user's information.
        """
        user = UsersModel(id=id, full_name=data['full_name'], username=data['username'],
                          email=data['email'], phone_number=data['phone_number'])
        response = user.update()
        return response

    @classmethod
    def delete_user(cls, id):
        """
        Deletes a user with the given ID.
        """
        response = UsersModel.delete(id)
        return response

# # Entities
# from src.models.entities.Users import User
# Models:
from src.models.ModelUser import ModelUser
from flask import Blueprint, request

# Database
from src.database.db_conection import connect_to_mysql
from src.utils.Security import Security

# Database connection:
db = connect_to_mysql()


user = Blueprint('user', __name__)


@user.route('/profile/<id>', methods=['GET'])
def get_profile_user(id):
    has_access = Security.verify_token(request.headers)
    if has_access:
        return has_access
    if request.method == 'GET':
        response = ModelUser.get_user_by_id(db, id)
        return response


@user.route('/update/<id>', methods=['POST'])
def update_user(id):
    has_access = Security.verify_token(request.headers)
    if has_access:
        return has_access
    if request.method == 'POST':
        data = request.json
        valid_data = ModelUser.validate_data_update(data)
        if valid_data:
            return valid_data
        response = ModelUser.update_user(db, id, data)
        return response

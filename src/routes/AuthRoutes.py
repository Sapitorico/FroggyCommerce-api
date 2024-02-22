from flask import Blueprint, request
from datetime import datetime
from uuid import uuid4

# Models:
from src.models.ModelUser import ModelUser

# Entities
from src.models.entities.Users import User


auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.json
        validation_error = ModelUser.validate_data_register(data)
        if validation_error:
            return validation_error
        user = User(full_name=data.get('full_name'),
                    email=data.get('email'),
                    password=User.hash_password(data.get('password')),
                    user_type='customer')
        response = ModelUser.register(user)
        return response


@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        validation_error = ModelUser.validate_data_login(data)
        if validation_error:
            return validation_error
        user = User(email=data.get('email'),
                    password=data.get('password'))
        response = ModelUser.login(user)
        return response

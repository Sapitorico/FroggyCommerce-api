import datetime
from flask import Flask, make_response, request, jsonify
import uuid
from flask_mysqldb import MySQL
from config import config
import re

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.Users import User

app = Flask(__name__)

db = MySQL(app)

@app.route('/')
def index():
    return '¡Hola, mundo!'
    
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.json
        validation_error = ModelUser.validate_data_register(data)
        if validation_error:
            return validation_error
        current_datetime = datetime.datetime.now()
        user = User(id=str(uuid.uuid4()),
                    full_name=data.get('full_name'),
                    email=data.get('email'),
                    password=User.hash_password(data.get('password')), 
                    user_type='customer', 
                    created_at=current_datetime)
        response = ModelUser.register(db, user)
        return response


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        validation_error = ModelUser.validate_data_login(data)
        if validation_error:
            return validation_error
        user = User(email=data.get('email'), 
                    password=data.get('password'))
        print(user.email, user.password)
        response = ModelUser.login(db, user)
        return response
        
        

        


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
from flask import Flask, make_response, request, jsonify
import uuid
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.functions.hash_password import hash_password
from flask_mysqldb import MySQL
from config import config
import re

app = Flask(__name__)

db = MySQL(app)


@app.route('/')
def index():
    return '¡Hola, mundo!'


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({"error": "No se proporcionaron datos."}), 400
    
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    
    missing_fields = [field for field in ['full_name', 'email', 'password'] if field not in data]
    if missing_fields:
        return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}."}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"error": "Formato de correo electrónico inválido."}), 400

    if len(password) < 8:
        return jsonify({"error": "La contraseña debe tener al menos 8 caracteres."}), 400

    if len(full_name.split(' ')) < 2:
        return jsonify({"error": "El nombre completo debe contener al menos nombre y apellido."}), 400
    
    hashed_password = hash_password(password)
    user_id = str(uuid.uuid4())
    
    try:
        cursor = db.connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            return jsonify({"error": "El usuario ya existe."}), 400

        sql = "INSERT INTO users (id, full_name, email, password, user_type) VALUES (%s, %s, %s, %s, 'customer')"
        cursor.execute(sql, (user_id, full_name, email, hashed_password))
        db.connection.commit()
    except Exception as e:
        return jsonify({"error": "Error de base de datos."}), 500
    finally:
        cursor.close()
    
    response = make_response(jsonify({"message": f'Usuario {full_name} registrado con éxito.'}), 200)
    return response




if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
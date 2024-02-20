import re
import uuid
from flask import jsonify
from datetime import datetime

# Security:
from src.utils.Security import Security

# Entities:
from src.models.entities.Users import User


class ModelUser():

    @classmethod
    def register(self, db, user):
        try:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email = %s", (user.email,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({"success": False, "message": "El usuario ya existe."}), 400
            sql = "INSERT INTO users (id, full_name, email, password, user_type, created_at) VALUES (%s, %s, %s, %s, 'customer', %s)"
            user_id = str(uuid.uuid4())
            cursor.execute(sql, (user_id, user.full_name, user.email,
                           user.password, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            db.commit()
        except Exception as e:
            raise Exception(
                f"Error al conectar con la base de datos: {str(e)}")
        finally:
            cursor.close()
            print("Connection closed")
        return jsonify({"success": True, "message": f'Usuario {user.full_name} registrado con éxito.'}), 200

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email = %s", (user.email,))
            existing_user = cursor.fetchone()
            if not existing_user:
                return jsonify({"success": False, "message": "Credenciales incorrectas."}), 400
            user = User(id=existing_user[0],
                        full_name=existing_user[1],
                        email=existing_user[2],
                        password=User.check_password(
                            existing_user[3], user.password),
                        user_type=existing_user[4],
                        created_at=existing_user[5])
            if user == None:
                return jsonify({"success": False, "message": "Credenciales incorrectas."}), 400
            if user.password == False:
                return jsonify({"success": False, "message": "Credenciales incorrectas."}), 400
            token = Security.getnerate_token(user)
            response_data = {
                "success": True,
                "message": "Inicio de sesión exitoso.",
                "user": user.to_dict(),
                "token": token
            }
            return jsonify(response_data), 200
        except Exception as e:
            raise Exception(
                f"Error al conectar con la base de datos: {str(e)}")
        finally:
            cursor.close()
            print("Connection closed")

    @classmethod
    def validate_data_register(self, data):
        if not data:
            return jsonify({"error": "No se proporcionaron datos."}), 400
        full_name = data.get('full_name')
        email = data.get('email')
        password = data.get('password')

        missing_fields = [field for field in [
            'full_name', 'email', 'password'] if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}."}), 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Formato de correo electrónico inválido."}), 400

        if len(password) < 8:
            return jsonify({"error": "La contraseña debe tener al menos 8 caracteres."}), 400

        if len(full_name.split(' ')) < 2:
            return jsonify({"error": "El nombre completo debe contener al menos nombre y apellido."}), 400

        return None

    @classmethod
    def validate_data_login(self, data):
        if not data:
            return jsonify({"error": "No se proporcionaron datos."}), 400
        email = data.get('email')
        password = data.get('password')

        missing_fields = [field for field in [
            'email', 'password'] if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}."}), 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Formato de correo electrónico inválido."}), 400

        if len(password) < 8:
            return jsonify({"error": "La contraseña debe tener al menos 8 caracteres."}), 400

        return None

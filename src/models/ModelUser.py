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
    def register(cls, db, user):
        try:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email = %s", (user.email,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({"success": False, "message": "Este usuario ya fue registrado"}), 400
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
        return jsonify({"success": True, "message": f'Usuario {user.full_name} registrado con éxito'}), 201

    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email = %s", (user.email,))
            existing_user = cursor.fetchone()
            if not existing_user:
                return jsonify({"success": False, "message": "Credenciales incorrectas"}), 400
            user = User(id=existing_user[0],
                        full_name=existing_user[1],
                        email=existing_user[2],
                        password=User.check_password(
                            existing_user[3], user.password),
                        user_type=existing_user[4],
                        created_at=existing_user[5])
            if user == None:
                return jsonify({"success": False, "message": "Credenciales incorrectas"}), 400
            if user.password == False:
                return jsonify({"success": False, "message": "Credenciales incorrectas"}), 400
            token = Security.getnerate_token(user)
            response_data = {
                "success": True,
                "message": "Inicio de sesión exitoso",
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
    def get_user_by_id(cls, db, id):
        try:
            cursor = db.cursor()
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql, (id,))
            user = cursor.fetchone()
            if not user:
                return jsonify({"success": False, "message": "Usuario no encontrado"}), 404
            user = User(id=user[0],
                        full_name=user[1],
                        email=user[2],
                        user_type=user[4],
                        created_at=user[5])
            return jsonify({"success": True, "user": user.to_dict()}), 200
        except Exception as e:
            raise Exception(
                f"Error al conectar con la base de datos: {str(e)}")
        finally:
            cursor.close()
            print("Connection closed")

    @classmethod
    def update_user(cls, db, id, data_user):
        try:
            cursor = db.cursor()
            sql = "UPDATE users SET "
            set_values = []
            values = []
            if 'full_name' in data_user:
                set_values.append("full_name = %s")
                values.append(data_user['full_name'])
            if 'email' in data_user:
                set_values.append("email = %s")
                values.append(data_user['email'])
            if 'password' in data_user:
                set_values.append("password = %s")
                values.append(data_user['password'])
            values.append(id)
            sql = f"UPDATE users SET {', '.join(set_values)} WHERE id = %s"
            cursor.execute(sql, tuple(values))
            db.commit()
            return jsonify({"success": True, "message": f'Usuario actualizado con éxito'}), 200
        except Exception as e:
            raise Exception(
                f"Error al conectar con la base de datos: {str(e)}")
        finally:
            cursor.close()
            print("Connection closed")

    @staticmethod
    def validate_data_update(data):
        if not data:
            return jsonify({"success": False, "message": "No se proporcionaron datos"}), 400

        required_fields = ['full_name', 'email', 'password']
        if not any(field in data for field in required_fields):
            return jsonify({"success": False, "message": "Campos admitidos: full_name, email, password"}), 400

        if "email" in data:
            invalid_email = User.validate_email(data['email'])
            if invalid_email:
                return invalid_email

        if "password" in data:
            invalid_password = User.validate_password(data['password'])
            if invalid_password:
                return invalid_password

        if 'full_name' in data:
            invalid_full_name = User.validate_full_name(data['full_name'])
            if invalid_full_name:
                return invalid_full_name

        return None

    @staticmethod
    def validate_data_register(data):
        if not data:
            return jsonify({"success": False, "message": "No se proporcionaron datos"}), 400

        missing_fields = [field for field in [
            'full_name', 'email', 'password'] if field not in data]
        if missing_fields:
            return jsonify({"success": False, "message": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

        if "email" in data:
            invalid_email = User.validate_email(data['email'])
            if invalid_email:
                return invalid_email

        if "password" in data:
            invalid_password = User.validate_password(data['password'])
            if invalid_password:
                return invalid_password

        if 'full_name' in data:
            invalid_full_name = User.validate_full_name(data['full_name'])
            if invalid_full_name:
                return invalid_full_name

        return None

    @staticmethod
    def validate_data_login(data):
        if not data:
            return jsonify({"success": False, "message": "No se proporcionaron datos"}), 400
        email = data.get('email')
        password = data.get('password')

        missing_fields = [field for field in [
            'email', 'password'] if field not in data]
        if missing_fields:
            return jsonify({"success": False, "message": f"Faltan los siguientes campos: {', '.join(missing_fields)}"}), 400

        if "email" in data:
            invalid_email = User.validate_email(data['email'])
            if invalid_email:
                return invalid_email

        if "password" in data:
            invalid_password = User.validate_password(data['password'])
            if invalid_password:
                return invalid_password

        return None

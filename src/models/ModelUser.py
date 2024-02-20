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
    def get_user_by_id(self, db, id):
        try:
            cursor = db.cursor()
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql, (id,))
            user = cursor.fetchone()
            if not user:
                return jsonify({"success": False, "message": "Usuario no encontrado."}), 404
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
    def update_user(self, db, id, data_user):
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
            if 'user_type' in data_user:
                set_values.append("user_type = %s")
                values.append(data_user['user_type'])
            if 'password' in data_user:
                set_values.append("password = %s")
                values.append(data_user['password'])
            values.append(id)
            sql = f"UPDATE users SET {', '.join(set_values)} WHERE id = %s"
            cursor.execute(sql, tuple(values))
            db.commit()
            return jsonify({"success": True, "message": f'Usuario actualizado con éxito.'}), 200
        except Exception as e:
            raise Exception(
                f"Error al conectar con la base de datos: {str(e)}")
        finally:
            # cursor.close()
            print("Connection closed")

    @classmethod
    def validate_data_update(cls, data):
        if not data:
            return jsonify({"success": False, "message": "No se proporcionaron datos."}), 400

        required_fields = ['full_name', 'email', 'user_type', 'password']
        if not any(field in data for field in required_fields):
            return jsonify({"success": False, "message": "Se debe proporcionar al menos uno de los siguientes campos: full_name, email, user_type, password."}), 400

        if 'email' in data and not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
            return jsonify({"success": False, "message": "Formato de correo electrónico inválido."}), 400

        if 'full_name' in data and len(data["full_name"].split(' ')) < 2:
            return jsonify({"success": False, "message": "El nombre completo debe contener al menos nombre y apellido."}), 400

        if 'user_type' in data and data["user_type"] not in ["admin", "customer"]:
            return jsonify({"success": False, "message": "El tipo de usuario debe ser 'admin' o 'customer'."}), 400

        if 'password' in data and len(data["password"]) < 8:
            return jsonify({"success": False, "message": "La contraseña debe tener al menos 8 caracteres."}), 400

        return None

    @classmethod
    def validate_data_register(self, data):
        if not data:
            return jsonify({"success": False, "message": "No se proporcionaron datos."}), 400
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

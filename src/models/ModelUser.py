import re
import uuid
from flask import jsonify, make_response

from .entities.Users import User

class ModelUser():
    
    @classmethod
    def register(self, db, user):     
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({"error": "El usuario ya existe."}), 400
            sql = "INSERT INTO users (id, full_name, email, password, user_type) VALUES (%s, %s, %s, %s, 'customer')"
            user_id = str(uuid.uuid4())
            cursor.execute(sql, (user_id, user.full_name, user.email, user.password))
            db.connection.commit()
        except Exception as e:
            return jsonify({"error": f"Error de base de datos: {str(e)}"}), 500
        finally:
            cursor.close()
        return make_response(jsonify({"message": f'Usuario {user.full_name} registrado con éxito.'}), 200)
    
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
            existing_user = cursor.fetchone()
            if not existing_user:
                return jsonify({"error": "Credenciales incorrectas."}), 400
            user = User(id=existing_user[0],
                        full_name=existing_user[1],
                        email=existing_user[2],
                        password=User.check_password(existing_user[3], user.password),
                        user_type=existing_user[4],
                        created_at=existing_user[5])
            if user == None:
                return jsonify({"error": "Credenciales incorrectas."}), 400
            if user.password == False:
                return jsonify({"error": "Credenciales incorrectas."}), 400
            return jsonify({"user": user.to_dict(), "message": "Inicio de sesión exitoso."}), 200
        except Exception as e:
            raise Exception(f"Error al conectar con la base de datos: {str(e)}")
        finally:
            cursor.close()
        
        
    @classmethod
    def get_user_by_email(self, db, email):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            raise Exception(f"Error al conectar con la base de datos: {str(e)}")
        finally:
            cursor.close()
            
    @classmethod
    def validate_data_register(self, data):
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
        
        return None;
    
    
    @classmethod
    def validate_data_login(self, data):
        if not data:
            return jsonify({"error": "No se proporcionaron datos."}), 400
        email = data.get('email')
        password = data.get('password')
        
        missing_fields = [field for field in ['email', 'password'] if field not in data]
        if missing_fields:
            return jsonify({"error": f"Faltan los siguientes campos: {', '.join(missing_fields)}."}), 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Formato de correo electrónico inválido."}), 400

        if len(password) < 8:
            return jsonify({"error": "La contraseña debe tener al menos 8 caracteres."}), 400

        return None;
        
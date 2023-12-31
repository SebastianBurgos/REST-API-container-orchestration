import os
import mysql.connector
import jwt
from datetime import datetime, timedelta
from app import app
from flask import request, jsonify
from modules.database import db
from modules.rabbitmqservice import enviar_mensaje_logs
from modules.utils import validar_token, evento_crear_perfil

# Clave secreta para la generación y verificación de tokens JWT
SECRET_KEY = os.environ.get("SECRET_KEY")

@app.route('/', methods=['GET'])
def index():
    return "API REST FUNCIONANDO"

# Metodo GET para obtener la lista de usuarios
# Para probar la paginación, puedes acceder a la URL /users y agregar 
# los parámetros page y per_page a la URL, por ejemplo: 
# /users?page=1&per_page=10 y opcionalmente &search_name=Sebas
@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Obtener los parámetros de paginación de la URL (opcional)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        search_name = request.args.get('search_name', '')

        # Calcular el índice de inicio y final para la paginación
        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        # Conectar a la base de datos
        cursor = db.cursor(dictionary=True)

        # Consulta SQL para obtener una página de usuarios
        query = "SELECT * FROM Usuario WHERE nombre LIKE %s LIMIT %s, %s"
        cursor.execute(query, (f"%{search_name}%", start_index, end_index))

        # Obtener los resultados y cerrar el cursor
        users = cursor.fetchall()
        cursor.close()

        # Retornar la lista de usuarios en formato JSON junto con información de paginación
        response = {
            "page": page,
            "per_page": per_page,
            "search_name": search_name,
            "users": users
        }
        
        mensaje = "SE HA CONSULTADO LA LISTA DE USUARIOS."
        metodo = "GET."
        ruta = "/users."
        ip = str(request.remote_addr)
        fecha = str(datetime.now())
        tipo_log = "INFO"
        modulo = "ROUTES.PY"
        application = "USERS_API_REST"
        usuario_autenticado = "GUEST"
        token = "NO TOKEN"
        enviar_mensaje_logs(tipo_log, metodo, ruta, modulo, application, fecha, ip, usuario_autenticado, token, mensaje)

        if any(users):
            return jsonify(response), 200
        else:
            return jsonify(response), 404

    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": "Error al obtener usuarios"}), 500

# Método POST para registrar usuarios
@app.route('/users', methods=['POST'])  
def register_user():
    try:
        data = request.get_json()  # Obtener datos del cuerpo de la solicitud JSON

        # Verificar si todos los campos requeridos están presentes en los datos
        required_fields = ['nombre', 'apellido', 'email', 'clave', 'fecha_nacimiento']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"El campo '{field}' es requerido"}), 400

        nombre = data.get('nombre')
        apellido = data.get('apellido')
        email = data.get('email')
        clave = data.get('clave')
        fecha_nacimiento = data.get('fecha_nacimiento')

        cursor = db.cursor(dictionary=True)
        query = "INSERT INTO Usuario (nombre, apellido, email, clave, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s)"
        values = (nombre, apellido, email, clave, fecha_nacimiento)
        cursor.execute(query, values)
        usuario_id = cursor.lastrowid
        db.commit()
        cursor.close()

        mensaje = "UN USUARIO SE HA REGISTRADO."
        metodo = "POST."
        ruta = "/users/register."
        ip = str(request.remote_addr)
        fecha = str(datetime.now())
        tipo_log = "AUTH"
        modulo = "ROUTES.PY"
        application = "USERS_API_REST"
        usuario_autenticado = "USUARIO REGISTRADO: "+nombre+" "+apellido
        token = "NO TOKEN"
        enviar_mensaje_logs(tipo_log, metodo, ruta, modulo, application, fecha, ip, usuario_autenticado, token, mensaje)
        evento_crear_perfil(usuario_id)

        return jsonify({"message": "Usuario registrado exitosamente"}), 201

    except mysql.connector.Error as err:
        print("Error:", str(err))
        return jsonify({"error": "Error al registrar usuario, razon: "+str(err)}), 500
    
# Método GET para obtener un usuario por su ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM Usuario WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404

    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": str(err)}), 500

# Método DELETE para eliminar un usuario por su ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    try:
        # Obtener el token del encabezado Authorization
        auth_header = request.headers.get('Authorization')

        # Llama a la función para validar el token
        valido, payload, error_code = validar_token(auth_header)

        if not valido:
            return jsonify(payload), error_code
        
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM Usuario WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            cursor = db.cursor(dictionary=True)
            query_delete = "DELETE FROM Usuario WHERE id = %s"
            cursor.execute(query_delete, (user_id,))
            db.commit()
            cursor.close()

            return jsonify({"message": "Usuario eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    
    except mysql.connector.Error as err:
        print("Error al eliminar el usuario:", err)
        return jsonify({"error": str(err)}), 500
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except (jwt.DecodeError, jwt.InvalidTokenError):
        return jsonify({"error": "Token inválido"}), 401

# Método PUT para actualizar un usuario por su ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    try:
        # Obtener el token del encabezado Authorization
        auth_header = request.headers.get('Authorization')

        # Llama a la función para validar el token
        valido, payload, error_code = validar_token(auth_header)

        if not valido:
            return jsonify(payload), error_code
    
        data = request.get_json()
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        email = data.get('email')
        fecha_nacimiento = data.get('fecha_nacimiento')

        # Construye la consulta SQL y los valores de manera dinámica
        query_update = "UPDATE Usuario SET "
        values = []
        if nombre is not None:
            query_update += "nombre = %s, "
            values.append(nombre)
        if apellido is not None:
            query_update += "apellido = %s, "
            values.append(apellido)
        if email is not None:
            query_update += "email = %s, "
            values.append(email)
        if fecha_nacimiento is not None:
            query_update += "fecha_nacimiento = %s, "
            values.append(fecha_nacimiento)

        # Elimina la coma extra al final de la consulta SQL
        query_update = query_update.rstrip(', ')

        # Agrega la condición WHERE para actualizar el usuario específico
        query_update += " WHERE id = %s"
        values.append(user_id)

        cursor = db.cursor(dictionary=True)
        # Ejecuta la consulta SQL con los valores
        cursor.execute(query_update, values)
        db.commit()
        cursor.close()

        return jsonify({"message": "Usuario actualizado exitosamente"}), 200
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": str(err)}), 500
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except (jwt.DecodeError, jwt.InvalidTokenError):
        return jsonify({"error": "Token inválido"}), 401
    

# Método POST para el login de usuario
@app.route('/auth', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data.get('email')
        clave = data.get('clave')

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM Usuario WHERE email = %s AND clave = %s"
        values = (email, clave)
        cursor.execute(query, values)

        user = cursor.fetchone()
        cursor.close()

        if user:
            # Generar token JWT con una duración de 30 minutos
            payload = {
                'user_id': user['id'],
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            mensaje = "UN USUARIO SE HA AUTENTICADO."
            metodo = "POST."
            ruta = "/auth."
            ip = str(request.remote_addr)
            fecha = str(datetime.now())
            tipo_log = "AUTH"
            modulo = "ROUTES.PY"
            application = "USERS_API_REST"
            usuario_autenticado = "[ID: "+str(user['id'])+"] "+user['nombre']+" "+user['apellido']

            enviar_mensaje_logs(tipo_log, metodo, ruta, modulo, application, fecha, ip, usuario_autenticado, token, mensaje)

            return jsonify({"token": token,
                            "id_user": user['id']}), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": "Error en el proceso de login"}), 500

# Método PATCH para actualizar la clave del usuario autenticado
#  Para probar este método, debes incluir el token JWT en el encabezado Authorization
#  de la solicitud con el formato "Bearer token".
#  Además, envía un JSON en el cuerpo de la solicitud con la nueva clave
@app.route('/users/<int:user_id>/new-password', methods=['PATCH'])
def change_password(user_id):
    try:
        # Obtener el token del encabezado Authorization
        auth_header = request.headers.get('Authorization')

        # Llama a la función para validar el token
        valido, payload, error_code = validar_token(auth_header)

        if not valido:
            return jsonify(payload), error_code

        data = request.get_json()
        nueva_clave = data.get('nueva_clave')

        cursor = db.cursor()
        query = "UPDATE Usuario SET clave = %s WHERE id = %s"
        values = (nueva_clave, user_id)
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return jsonify({"message": "Clave actualizada exitosamente"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except (jwt.DecodeError, jwt.InvalidTokenError):
        return jsonify({"error": "Token inválido"}), 401
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": "Error al actualizar la clave"}), 500

# Método POST para recuperar la clave de un usuario
@app.route('/auth/password-reset', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')

        cursor = db.cursor(dictionary=True)
        query = "SELECT id FROM Usuario WHERE email = %s"
        cursor.execute(query, (email,))

        user = cursor.fetchone()
        cursor.close()

        if user:
            # Generar un token de recuperación de clave con una duración de 1 hora
            payload = {
                'user_id': user['id'],
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({"token": token}), 200
        else:
            return jsonify({"error": "Correo electrónico no encontrado"}), 404

    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": "Error en el proceso de recuperación de clave"}), 500
    
@app.route('/health')
def health_check():
    return 'health check'
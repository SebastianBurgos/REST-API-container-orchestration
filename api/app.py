import time
import mysql.connector
import os
import jwt
import pika
from datetime import datetime, timedelta
from insertions import data
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración de la base de datos
def esperar_db():
    while True:
        try:
            db = mysql.connector.connect(
                host=os.environ.get("SERVICE"),
                user=os.environ.get("USER"),
                password=os.environ.get("PASSWORD"),
                database=os.environ.get("DATABASE"),
            )
            return db
        except mysql.connector.Error as err:
            print("Error:", err)
            print("Reintentando conexión a la base de datos en 5 segundos...")
            time.sleep(5)

def esperar_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ.get("RABBITMQ_SERVICE"), heartbeat=600)
            )
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Reintentando conexión a RabbitMQ en 5 segundos...")
            time.sleep(5)

db = esperar_db()
gestormensajes = esperar_rabbitmq()
channel = gestormensajes.channel()
nombre_servicio = os.environ.get("SERVICE_NAME")

# Declarar una cola
channel.queue_declare(queue='autenticaciones')

# Declaramos la función para envio de mensajes
def enviar_mensaje(mensaje, metodo, ruta, username, fecha):
    bodymensaje = nombre_servicio+"#"+mensaje+"#"+metodo+"#"+ruta+"#"+username+"#"+fecha
    channel.basic_publish(exchange='', routing_key='autenticaciones', body=bodymensaje)
    print(f"Mensaje enviado: Usuario: {username}\nMensaje: {mensaje}")

# Insertar datos falsos en la base de datos
def insertFakeData():
    try:
        cursor = db.cursor()
        print("Insertando datos falsos en la base de datos...")
        cursor.executemany("""INSERT INTO Usuario (nombre, apellido, email, clave, fecha_nacimiento) 
                            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(clave)s, %(fecha_nacimiento)s)""", data)
        db.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print("Error:", err)

insertFakeData()

# Clave secreta para la generación y verificación de tokens JWT
SECRET_KEY = "microchervices"

print("Todo bien")

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
        cursor.execute(query, (f"%{search_name}%", start_index, per_page))

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
        
        mensaje = "Se ha consultado la lista de usuarios."
        metodo = "GET."
        ruta = "/users."
        username = str(request.remote_addr)
        fecha = str(datetime.now())
        enviar_mensaje(mensaje, metodo, ruta, username, fecha)

        if any(users):
            return jsonify(response), 200
        else:
            return jsonify({"error":"Error al obtener usuarios"}), 404

    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": "Error al obtener usuarios"}), 500


# Método POST para registrar usuarios
@app.route('/users/register', methods=['POST'])  
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

        cursor = db.cursor()
        query = "INSERT INTO Usuario (nombre, apellido, email, clave, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s)"
        values = (nombre, apellido, email, clave, fecha_nacimiento)
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return jsonify({"message": "Usuario registrado exitosamente"}), 201

    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": "Error al registrar usuario"}), 500
    
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
        return jsonify({"error": "Error al obtener el usuario"}), 500

# Método DELETE para eliminar un usuario por su ID
@app.route('/users', methods=['DELETE'])
def delete_user_by_id():
    try:
        # Obtener el token del encabezado Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return jsonify({"error": "Token de autorización faltante"}), 401
        
        token = auth_header.split(' ')[1]  # Eliminar la palabra "Bearer" del token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # Obtener el ID del usuario autenticado
        user_id = payload.get('user_id')

        cursor = db.cursor()
        query_delete = "DELETE FROM Usuario WHERE id = %s"
        cursor.execute(query_delete, (user_id,))
        db.commit()
        cursor.close()

        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": "Error al eliminar el usuario"}), 500
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except (jwt.DecodeError, jwt.InvalidTokenError):
        return jsonify({"error": "Token inválido"}), 401

# Método PUT para actualizar un usuario por su ID
@app.route('/users', methods=['PUT'])
def update_user_by_id():
    try:
        # Obtener el token del encabezado Authorization
        auth_header = request.headers.get('Authorization')

        if auth_header is None:
            return jsonify({"error": "Token de autorización faltante"}), 401
        cursor = db.cursor(dictionary=True)
        
        token = auth_header.split(' ')[1]  # Eliminar la palabra "Bearer" del token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

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
        values.append(payload.get('user_id'))

        # Ejecuta la consulta SQL con los valores
        cursor.execute(query_update, values)
        db.commit()
        cursor.close()

        return jsonify({"message": "Usuario actualizado exitosamente"}), 200
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify({"error": "Error al actualizar el usuario"}), 500
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except (jwt.DecodeError, jwt.InvalidTokenError):
        return jsonify({"error": "Token inválido"}), 401
    

# Método POST para el login de usuario
@app.route('/tokens', methods=['POST'])
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
@app.route('/users/user/new-password', methods=['PATCH'])
def change_password():
    try:
        # Obtener el token del encabezado Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return jsonify({"error": "Token de autorización faltante"}), 401

        token = auth_header.split(' ')[1]  # Eliminar la palabra "Bearer" del token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # Obtener el ID del usuario autenticado
        user_id = payload.get('user_id')

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
@app.route('/tokens/token-password', methods=['POST'])
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

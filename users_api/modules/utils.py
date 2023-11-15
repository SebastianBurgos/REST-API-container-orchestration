import os
import jwt
import mysql.connector
import requests
from modules.database import db

# Clave secreta para la generación y verificación de tokens JWT
SECRET_KEY = os.environ.get("SECRET_KEY")

# Función para validar el token
def validar_token(auth_header):
    if auth_header is None:
        return False, {"error": "Token de autorización faltante"}, 401

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True, payload, None
    except jwt.ExpiredSignatureError:
        return False, {"error": "Token expirado"}, 401
    except jwt.InvalidTokenError:
        return False, {"error": "Token inválido"}, 401

def evento_crear_perfil(usuario_id):
    try:
        usuario_datos = obtener_usuario_por_id(usuario_id)

        # Convierte los datos del usuario a un formato JSON
        usuario_json = {
            "id": usuario_datos["id"],
            "nombre": usuario_datos["nombre"],
            "apellido": usuario_datos["apellido"],
            "email": usuario_datos["email"]
        }

        # Llama a la función para enviar la solicitud POST
        enviar_solicitud_post(usuario_json)

    except mysql.connector.Error as err:
        print("Error en el evento crear perfil: ", err)

def obtener_usuario_por_id(usuario_id):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM Usuario WHERE id = %s"
    values = (usuario_id,)
    cursor.execute(query, values)
    usuario_datos = cursor.fetchone()
    return usuario_datos

def enviar_solicitud_post(usuario_json):
    url = "http://profiles_api:4000/profiles"

    # Realiza la solicitud POST con los datos del usuario como JSON
    response = requests.post(url, json=usuario_json)

    # Verifica el código de estado de la respuesta
    if response.status_code == 201:
        print("Perfil creado exitosamente.")
    else:
        print(f"Error al crear el perfil. Código de estado: {response.status_code}")


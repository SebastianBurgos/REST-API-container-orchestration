import os
import jwt

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
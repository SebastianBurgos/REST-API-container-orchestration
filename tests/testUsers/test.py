import requests

URL = "http://localhost:5000"

# Obtener una lista de todos los usuarios
def test_obtener_lista_usuarios():
    # Define el endpoint para obtener la lista de usuarios
    endpoint = "/users"

    # Realiza la solicitud GET a tu API local
    response = requests.get(URL + endpoint)

    # Verifica el código de estado
    assert response.status_code == 200

    # Verifica que la respuesta sea exitosa y contenga una lista de usuarios
    data = response.json()
    assert "users" in data

def test_obtener_lista_usuarios_vacia():
    # Define el valor del parámetro "page"
    page = 100  # Ajusta el valor según tus necesidades

    # Define el endpoint para obtener la lista de usuarios con el parámetro "page"
    endpoint = f"/users?page={page}"

    # Realiza la solicitud GET a tu API local
    response = requests.get(URL + endpoint)

    # Verifica el código de estado
    assert response.status_code == 404

    # Verifica que la respuesta contenga un mensaje de alerta
    data = response.json()
    assert data['users'] == []


# Escenario en Gherkin
def test_obtener_lista_usuarios_con_nombre():
    # Define el nombre que el usuario proporcionará
    nombre_usuario = "Ana"

    # Define el endpoint para obtener la lista de usuarios con el nombre especificado
    endpoint = f"/users?search_name={nombre_usuario}"

    # Realiza la solicitud GET a tu API local
    response = requests.get(URL + endpoint)

    # Verifica el código de estado
    assert response.status_code == 200

    # Verifica que la respuesta contenga una lista de usuarios con el nombre especificado
    data = response.json()
    assert "users" in data
    for user in data["users"]:
        assert nombre_usuario.lower() in user["nombre"].lower()

def test_registrar_nuevo_usuario():
    # Define los datos de registro del usuario
    datos_registro = {
        "nombre": "Juan",
        "apellido": "Zambrano",
        "email": "JuanZ23@example.com",
        "clave": "contrasena123",
        "fecha_nacimiento": "2000-01-01"
    }

    # Define el endpoint para registrar un nuevo usuario
    endpoint = "/users"

    # Realiza la solicitud POST a tu API local
    response = requests.post(URL + endpoint, json=datos_registro)

    # Verifica el código de estado
    assert response.status_code == 201

    # Verifica que la respuesta contenga un mensaje de confirmación
    data = response.json()
    assert "message" in data
    assert "Usuario registrado exitosamente" in data["message"]

def test_usuario_falta_datos_registro():
    # Define los datos de registro del usuario sin la fecha de nacimiento
    datos_registro = {
        "nombre": "Nuevo",
        "apellido": "Usuario",
        "email": "nuevo@example.com",
        "clave": "contrasena123"
    }

    # Define el endpoint para registrar un nuevo usuario
    endpoint = "/users"

    # Realiza la solicitud POST a tu API local
    response = requests.post(URL + endpoint, json=datos_registro)

    # Verifica el código de estado
    assert response.status_code == 400

    # Verifica que la respuesta contenga un mensaje de alerta y el dato faltante
    data = response.json()
    assert "error" in data
    assert "El campo 'fecha_nacimiento' es requerido" in data["error"]

def test_usuario_formato_fecha_erroneo():
    # Define los datos de registro del usuario con un formato de fecha incorrecto
    datos_registro = {
        "nombre": "Sebastian",
        "apellido": "Puentes",
        "email": "PuentesSebas@example.com",
        "clave": "contrasena123",
        "fecha_nacimiento": "10-10-2000"  # Formato de fecha incorrecto
    }

    # Define el endpoint para registrar un nuevo usuario
    endpoint = "/users"

    # Realiza la solicitud POST a tu API local
    response = requests.post(URL + endpoint, json=datos_registro)

    # Verifica el código de estado
    assert response.status_code == 500

    # Verifica que la respuesta contenga un mensaje de error y el formato de fecha correcto
    data = response.json()
    assert "error" in data
    assert "Error al registrar usuario" in data["error"]

def test_buscar_usuario_por_id():
    # Define un ID de usuario existente en tu base de datos
    user_id = 1  # Ajusta el ID según tus necesidades

    # Define el endpoint para buscar un usuario por su ID
    endpoint = f"/users/{user_id}"

    # Realiza la solicitud GET a tu API local
    response = requests.get(URL + endpoint)

    # Verifica el código de estado
    assert response.status_code == 200

    # Verifica que la respuesta contenga la información del usuario
    data = response.json()
    assert "id" in data
    assert "nombre" in data
    assert "apellido" in data
    assert "email" in data
    assert "fecha_nacimiento" in data

def test_buscar_usuario_por_id_failed():
    # Define un ID de usuario NO existente en tu base de datos
    user_id = 250

    # Define el endpoint para buscar un usuario por su ID
    endpoint = f"/users/{user_id}"

    # Realiza la solicitud GET a tu API local
    response = requests.get(URL + endpoint)

    # Verifica el código de estado
    assert response.status_code == 404

    # Verifica que la respuesta contenga la información del usuario
    data = response.json()
    assert "error" in data
    assert "Usuario no encontrado" in data["error"]

def test_eliminar_cuenta_sin_autenticarse():
    # No se realiza la autenticación y no se obtiene un token JWT

    # Define un ID de usuario existente en tu base de datos
    user_id = 6  # Ajusta el ID según tus necesidades

    # Define el endpoint para buscar un usuario por su ID
    endpoint = f"/users/{user_id}"

    # Realiza la solicitud DELETE a tu API local sin encabezado de autorización
    delete_response = requests.delete(URL + endpoint)

    # Verifica el código de estado, debe ser 401 (no autorizado)
    assert delete_response.status_code == 401

    # Verifica que la respuesta contenga un mensaje de error
    delete_data = delete_response.json()
    assert "error" in delete_data
    assert "Token de autorización faltante" in delete_data["error"]


def test_actualizar_datos_usuario():
    # Define las credenciales del usuario autenticado (email y contraseña)
    email = "JuanZ23@example.com"  # Ajusta el email según tus necesidades
    clave = "contrasena123"  # Ajusta la contraseña según tus necesidades

    # Define el token JWT previamente autenticado
    token = obtener_token_jwt(email, clave)

    # Define los datos que el usuario desea actualizar
    nuevos_datos = {
        "nombre": "Alejandro",
        "apellido": "Armanda"
    }

    # Define el encabezado de autorización con el token JWT
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Define un ID de usuario existente en tu base de datos
    user_id = 6

    # Define el endpoint para actualizar la información del usuario
    endpoint = f"/users/{user_id}"

    # Realiza la solicitud PUT a tu API local con los nuevos datos y el encabezado de autorización
    put_response = requests.put(URL + endpoint, json=nuevos_datos, headers=headers)

    # Verifica el código de estado
    assert put_response.status_code == 200

    # Verifica que la respuesta contenga un mensaje de confirmación
    put_data = put_response.json()
    assert "message" in put_data
    assert "Usuario actualizado exitosamente" in put_data["message"]

def autenticacion_token(email, clave):
    # Realiza la autenticación y obtén el token JWT
    auth_payload = {
        "email": email,
        "clave": clave
    }
    auth_response = requests.post(URL + "/auth", json=auth_payload)

    # Verifica que la autenticación sea exitosa y obtén el token
    assert auth_response.status_code == 200
    auth_data = auth_response.json()
    assert "token" in auth_data
    token = auth_data["token"]
    return token


def test_actualizar_datos_sin_autenticar():
    # No se realiza la autenticación y no se obtiene un token JWT

    # Define los nuevos datos que el usuario desea actualizar
    nuevos_datos = {
        "nombre": "Burgos",  # Nuevo nombre
        "apellido": "Puentes"  # Nuevo apellido
    }

    # Define un ID de usuario existente en tu base de datos
    user_id = 6

    # Define el endpoint para actualizar la información del usuario (sin autorización)
    endpoint = f"/users/{user_id}"

    # Realiza la solicitud PUT a tu API local con los nuevos datos sin encabezado de autorización
    put_response = requests.put(URL + endpoint, json=nuevos_datos)

    # Verifica el código de estado, debe ser 401 (Solicitud incorrecta)
    assert put_response.status_code == 401

    # Verifica que la respuesta contenga un mensaje de error
    put_data = put_response.json()
    assert "error" in put_data
    assert "Token de autorización faltante" in put_data["error"]

def test_ingresar_sesion_exitosa():
    # Define los datos de inicio de sesión (Email y contraseña)
    datos_inicio_sesion = {
        "email": "JuanZ23@example.com",
        "clave": "contrasena123"
    }

    # Define el endpoint para iniciar sesión
    endpoint = "/auth"

    # Realiza la solicitud POST a tu API local con los datos de inicio de sesión
    response = requests.post(URL + endpoint, json=datos_inicio_sesion)

    # Verifica el código de estado, debe ser 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta contenga un token JWT válido y el ID del usuario
    data = response.json()
    assert "token" in data
    assert "id_user" in data

def test_ingresar_sesion_contraseña_incorrecta():
    # Define los datos de inicio de sesión (Email y contraseña incorrecta)
    datos_inicio_sesion = {
        "email": "correo@example.com",  # Ajusta el Email según tus necesidades
        "clave": "contrasena_incorrecta"  # Contraseña incorrecta
    }

    # Define el endpoint para iniciar sesión
    endpoint = "/auth"

    # Realiza la solicitud POST a tu API local con los datos de inicio de sesión incorrectos
    response = requests.post(URL + endpoint, json=datos_inicio_sesion)

    # Verifica el código de estado, debe ser 400 (error de solicitud)
    assert response.status_code == 401

    # Verifica que la respuesta contenga un mensaje de error indicando que la contraseña es incorrecta
    data = response.json()
    assert "error" in data
    assert "Credenciales inválidas" in data["error"]

def test_cambiar_contraseña_exitosamente():
    # Define los datos de inicio de sesión (Email y contraseña correcta)
    datos_inicio_sesion = {
        "email": "JuanZ23@example.com",  # Ajusta el Email según tus necesidades
        "clave": "contraseña123"  # Contraseña correcta
    }

    # Define el endpoint para iniciar sesión y obtener el token JWT
    endpoint_sesion = "/auth"

    # Realiza la solicitud POST a tu API local para obtener el token JWT
    response_sesion = requests.post(URL + endpoint_sesion, json=datos_inicio_sesion)

    # Verifica que la autenticación sea exitosa y obtén el token JWT
    assert response_sesion.status_code == 200
    data_sesion = response_sesion.json()
    assert "token" in data_sesion
    token = data_sesion["token"]

    # Define los datos de la nueva contraseña
    nueva_contraseña = {
        "nueva_clave": "nueva_contraseña123"  # Nueva contraseña
    }

    # Define el encabezado de autorización con el token JWT
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Define un ID de usuario existente en tu base de datos
    user_id = 6

    # Define el endpoint para cambiar la contraseña
    endpoint_cambio_contraseña = f"/users/{user_id}/new-password"

    # Realiza la solicitud PATCH a tu API local para cambiar la contraseña
    response_cambio_contraseña = requests.patch(URL + endpoint_cambio_contraseña, json=nueva_contraseña, headers=headers)

    # Verifica el código de estado, debe ser 200 (éxito)
    assert response_cambio_contraseña.status_code == 200

    # Verifica que la respuesta contenga un mensaje de confirmación
    data_cambio_contraseña = response_cambio_contraseña.json()
    assert "message" in data_cambio_contraseña
    assert "Clave actualizada exitosamente" in data_cambio_contraseña["message"]

def test_cambiar_contraseña_sin_autenticación():
    # No se realiza la autenticación y no se obtiene un token JWT

    # Define los datos de la nueva contraseña
    nueva_contraseña = {
        "nueva_clave": "nueva_contraseña123"  # Nueva contraseña
    }

    # Define un ID de usuario existente en tu base de datos
    user_id = 6

    # Define el endpoint para cambiar la contraseña (sin autorización)
    endpoint_cambio_contraseña = f"/users/{user_id}/new-password"

    # Realiza la solicitud PATCH a tu API local para cambiar la contraseña sin encabezado de autorización
    response_cambio_contraseña = requests.patch(URL + endpoint_cambio_contraseña, json=nueva_contraseña)

    # Verifica el código de estado, debe ser 401 (no autorizado)
    assert response_cambio_contraseña.status_code == 401

    # Verifica que la respuesta contenga un mensaje de error
    data_cambio_contraseña = response_cambio_contraseña.json()
    assert "error" in data_cambio_contraseña
    assert "Token de autorización faltante" in data_cambio_contraseña["error"]

def test_recuperar_contraseña():
    # Define el correo del usuario que desea recuperar su contraseña
    correo_usuario = "ana@example.com"  # Reemplaza con el correo del usuario

    # Define los datos del usuario para solicitar la recuperación de contraseña
    datos_solicitud_recuperación = {
        "email": correo_usuario
    }

    # Define el endpoint para solicitar la recuperación de contraseña
    endpoint_solicitar_recuperación = "/auth/password-reset"

    # Realiza la solicitud POST a tu API local para solicitar la recuperación de contraseña
    response_solicitar_recuperación = requests.post(URL + endpoint_solicitar_recuperación, json=datos_solicitud_recuperación)

    # Verifica el código de estado, debe ser 200 (éxito)
    assert response_solicitar_recuperación.status_code == 200

    # Verifica que la respuesta contenga un token de recuperación
    data_solicitar_recuperación = response_solicitar_recuperación.json()
    assert "token" in data_solicitar_recuperación


def test_eliminar_cuenta_usuario():
    # Define las credenciales del usuario autenticado (email y contraseña)
    email = "JuanZ23@example.com"
    clave = "nueva_contraseña123"

    # Realiza la autenticación y obtén el token JWT
    auth_payload = {
        "email": email,
        "clave": clave
    }
    auth_response = requests.post(URL + "/tokens", json=auth_payload)

    # Verifica que la autenticación sea exitosa y obtén el token
    assert auth_response.status_code == 200
    auth_data = auth_response.json()
    assert "token" in auth_data
    token = auth_data["token"]

    # Define el encabezado de autorización con el token JWT
    headers = {
        "Authorization": f"Bearer {token}"
    }

    user_id = 6  # Ajusta el ID según tus necesidades

    # Define el endpoint para eliminar la cuenta del usuario autenticado
    endpoint = f"/users/{user_id}"

    # Realiza la solicitud DELETE a tu API local con el encabezado de autorización
    delete_response = requests.delete(URL + endpoint, headers=headers)

    # Verifica el código de estado
    assert delete_response.status_code == 200

    # Verifica que la respuesta contenga un mensaje de despedida
    delete_data = delete_response.json()
    assert "message" in delete_data
    assert "Usuario eliminado exitosamente" in delete_data["message"]
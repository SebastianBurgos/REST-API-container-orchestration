import requests

URL = "http://localhost:8080"


def test_ingresar_sesion_exitosa():
    # Define los datos de inicio de sesión (Email y contraseña)
    datos_inicio_sesion = {
        "clave": "juan",
        "email": "juan@example.com"
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


def test_ingresar_sesion_fallida():
    # Define los datos de inicio de sesión (Email y contraseña)
    datos_inicio_sesion = {
        "clave": "juan1234",
        "email": "juan@example.com"
    }

    # Define el endpoint para iniciar sesión
    endpoint = "/auth"

    # Realiza la solicitud POST a tu API local con los datos de inicio de sesión
    response = requests.post(URL + endpoint, json=datos_inicio_sesion)

    # Verifica el código de estado, debe ser 200 (éxito)
    assert response.status_code == 500

def test_registrar_nuevo_usuario():
    # Define los datos de registro del usuario
    datos_registro = {
        "nombre": "User",
        "apellido": "Prueba",
        "email": "PruebaUsers@example.com",
        "clave": "contrasena123",
        "fecha_nacimiento": "2000-01-01"
    }

    # Define el endpoint para registrar un nuevo usuario
    endpoint = "/register"

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
    endpoint = "/register"

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
    endpoint = "/register"

    # Realiza la solicitud POST a tu API local
    response = requests.post(URL + endpoint, json=datos_registro)

    # Verifica el código de estado
    assert response.status_code == 500

    # Verifica que la respuesta contenga un mensaje de error y el formato de fecha correcto
    data = response.json()
    assert "error" in data
    assert "Error al registrar usuario" in data["error"]


#Ingresar sesion en el perfil
def test_ingresar_sesion_exitosa_profiles():
    # Define los datos de inicio de sesión (Email y contraseña)
    datos_inicio_sesion = {
        "clave": "juan",
        "email": "juan@example.com"
    }

    # Define el endpoint para iniciar sesión
    endpoint = "/auth-profiles"

    # Realiza la solicitud POST a tu API local con los datos de inicio de sesión
    response = requests.post(URL + endpoint, json=datos_inicio_sesion)

    # Verifica el código de estado, debe ser 200 (éxito)
    assert response.status_code == 200

    # Verifica que la respuesta contenga un token JWT válido y el ID del usuario
    data = response.json()
    assert "auth_data" in data
    assert "profile_data" in data


def test_ingresar_sesion_fallida_profiles():
    # Define los datos de inicio de sesión (Email y contraseña)
    datos_inicio_sesion = {
        "clave": "juan1234",
        "email": "juan@example.com"
    }

    # Define el endpoint para iniciar sesión
    endpoint = "/auth-profiles"

    # Realiza la solicitud POST a tu API local con los datos de inicio de sesión
    response = requests.post(URL + endpoint, json=datos_inicio_sesion)

    # Verifica el código de estado, debe ser 200 (éxito)
    assert response.status_code == 500


def test_update_profile():
    # Datos para la actualización del perfil
    datos_inicio_sesion = {
        "email" : "juan@example.com",  
        "clave" : "juan" ,
    }

    datos_perfil = {
        "url_pagina": "pedrito@gmail.com",
        "apodo": "Pedronel Suarez",
        "informacion_publica": 1,
        "direccion_correspondencia": "N/A",
        "biografia": "N/A",
        "organizacion": "N/A",
        "pais": "N/A"
    }


    # Hacer la solicitud PUT al endpoint de actualización de perfil
    response = requests.post(f"{URL}/update-profile", json={"auth_data": datos_inicio_sesion, "profile_data": datos_perfil})

    # Validar la respuesta
    assert response.status_code == 200 
    data = response.json()
    assert "auth_data" in data
    assert "updates_profile_response" in data


def test_update_profile_fail():
    # Datos para la actualización del perfil
    datos_inicio_sesion = {
        "email" : "juan@example.com",  
        "clave" : "juan123" ,
    }

    datos_perfil = {
        "url_pagina": "pedrito@gmail.com",
        "apodo": "Pedronel Suarez",
        "informacion_publica": 1,
        "direccion_correspondencia": "N/A",
        "biografia": "N/A",
        "organizacion": "N/A",
        "pais": "N/A"
    }


    # Hacer la solicitud PUT al endpoint de actualización de perfil
    response = requests.post(f"{URL}/update-profile", json={"auth_data": datos_inicio_sesion, "profile_data": datos_perfil})

    # Validar la respuesta
    assert response.status_code == 500 


def test_eliminar_cuenta_usuario():
    # Define las credenciales del usuario autenticado (email y contraseña)
    URL2 = "http://localhost:5000"
    email = "PruebaUsers@example.com"
    clave = "contrasena123"

    # Realiza la autenticación y obtén el token JWT
    auth_payload = {
        "email": email,
        "clave": clave
    }
    auth_response = requests.post(URL2 + "/auth", json=auth_payload)

    # Verifica que la autenticación sea exitosa y obtén el token
    assert auth_response.status_code == 200
    auth_data = auth_response.json()
    assert "token" in auth_data
    token = auth_data["token"]

    # Define el encabezado de autorización con el token JWT
    headers = {
        "Authorization": f"Bearer {token}"
    }

    user_id = auth_data['id_user']  # Ajusta el ID según tus necesidades

    # Define el endpoint para eliminar la cuenta del usuario autenticado
    endpoint = f"/users/{user_id}"

    # Realiza la solicitud DELETE a tu API local con el encabezado de autorización
    delete_response = requests.delete(URL2 + endpoint, headers=headers)

    # Verifica el código de estado
    assert delete_response.status_code == 200

    # Verifica que la respuesta contenga un mensaje de despedida
    delete_data = delete_response.json()
    assert "message" in delete_data
    assert "Usuario eliminado exitosamente" in delete_data["message"]

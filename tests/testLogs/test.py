import requests

URL = "http://localhost:5005"

# Obtener una lista con todos los logs
def test_Obtener_lista_logs():
    # Definir ruta
    endpoint = "/logs"

    # Realizar la solicitud Get
    response = requests.get(URL + endpoint)

    # Verificar el código de estado
    assert response.status_code == 200

    # Verificar la respuesta sea exitosa
    data = response.json()
    assert "logs" in data

# Registar logs
def test_Registrar_logs():
    # Define los datos de registro
    datos_registro = {
        "ACCION": "dolor amet Lorem",
        "APLICACION": "officia do in proident",
        "FECHA": "2023-10-03T00:00:00.0Z",
        "IP": "172.18.0.1",
        "METODO-HTTP": "ea eu eiusmod minim",
        "MODULO": "qui ex",
        "RUTA": "enim nostrud ullamco labore minim",
        "TIPO-LOG": "cupidatat in eu laboris dolor",
        "USUARIO-AUTENTICADO": "anim exercitation et",
        "TOKEN": "incididunt nulla consectetur aute Duis"
    }

    # Definir ruta
    endpoint = "/logs"

    # Realizar la solicitud POST
    response = requests.post(URL + endpoint, json=datos_registro)

    # Verifica el codigo de estado 
    assert response.status_code == 201

    # Verifica que la espuesta contega un mensaje de confirmación
    data = response.json()
    assert "message" in data
    assert "Log registrado exitosamente" in data["message"]

# Registar logs dato faltante
def test_Registrar_logs_NoData():
    # Define los datos de registro
    datos_registro = {
        "ACCION": "",
        "APLICACION": "officia do in proident",
        "FECHA": "2023-10-03T00:00:00.0Z",
        "IP": "172.18.0.1",
        "METODO-HTTP": "ea eu eiusmod minim",
        "MODULO": "qui ex",
        "RUTA": "enim nostrud ullamco labore minim",
        "TIPO-LOG": "cupidatat in eu laboris dolor",
        "USUARIO-AUTENTICADO": "anim exercitation et",
        "TOKEN": "incididunt nulla consectetur aute Duis"
    }

    # Definir ruta
    endpoint = "/logs"

    # Realizar la solicitud POST
    response = requests.post(URL + endpoint, json=datos_registro)

    # Verifica el codigo de estado 
    assert response.status_code == 400

    # Verifica que la espuesta contega un mensaje de confirmación
    data = response.json()
    assert "error" in data
    assert "El campo 'ACCION' es requerido" in data["error"]


# Obtener una lista con todos los logs por nombre
def test_Obtener_lista_logs_name():

    # Nombre de la applicación
    nombre_App = "USERS_API_REST"

    # Definir ruta
    endpoint = f"/logs"

    # Realizar la solicitud Get
    response = requests.get(URL + endpoint)

    # Verificar el código de estado
    assert response.status_code == 200

    # Verificar la respuesta sea exitosa
    data = response.json()
    assert "logs" in data
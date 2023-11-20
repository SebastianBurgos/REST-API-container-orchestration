import requests
import pytest

BASE_URL = "http://localhost:4000"  # Reemplaza con la URL de tu API local


# Como usuario quiero obtener una lista de los perfiles para mostrarlos
def test_obtener_lista_perfiles():
    # Realiza la solicitud GET a tu API local para obtener la lista de perfiles
    endpoint = "/profiles"

    response = requests.get(BASE_URL + endpoint)

    # Verifica el código de estado
    assert response.status_code == 200

    # Verifica que la respuesta contenga una lista de perfiles
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Verifica que la lista no esté vacía
    

def test_get_profile_successful():
    # Supongamos que tienes un usuario existente con ID 1 en tu base de datos
    id_perfil = 1

    email = "pricekatherine@example.net"  # Ajusta el email según tus necesidades
    clave = "+6)EIuRf%)" 

    token = obtener_token(email, clave)

    # Asegúrate de que este token sea válido y esté autenticado
    headers = {
       "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{BASE_URL}/profiles/{id_perfil}", headers=headers)

    assert response.status_code == 200
    assert "id" in response.json()  # Asegúrate de que la respuesta contiene la información del perfil


def test_get_profile_no():
    # Supongamos que tienes un usuario existente con ID 1 en tu base de datos
    id_perfil = 1000

    email = "pricekatherine@example.net"  # Ajusta el email según tus necesidades
    clave = "+6)EIuRf%)" 

    token = obtener_token(email, clave)

    # Asegúrate de que este token sea válido y esté autenticado
    headers = {
       "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{BASE_URL}/profiles/{id_perfil}", headers=headers)

    assert response.status_code == 404

    assert 'mensaje' in response.json() and response.json()['mensaje'] == 'No se encontró el perfil'


def test_get_profile_noLogin():
    # Supongamos que tienes un usuario existente con ID 1 en tu base de datos
    id_perfil = 1

    response = requests.get(f"{BASE_URL}/profiles/{id_perfil}")

    assert response.status_code == 401

    assert 'mensaje' in response.json() and response.json()['mensaje'] == 'No autorizado, token no existente'


def test_update_profile():
    id_perfil = 1
    email = "juan@example.com"  # Ajusta el email según tus necesidades
    clave = "juan" 
    token = obtener_token(email, clave)

    # Asegurarse de que este token sea válido y esté autenticado
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Datos para la actualización del perfil
    payload = {
        "apodo": "NuevoApodo",
        "informacion_publica": "Nueva información",
    }

    # Hacer la solicitud PUT al endpoint de actualización de perfil
    response = requests.put(f"{BASE_URL}/profiles/{id_perfil}", json=payload, headers=headers)

    # Validar la respuesta
    assert response.status_code == 200 
    assert 'mensaje' in response.json() and response.json()['mensaje'] == 'Perfil actualizado exitosamente'



def obtener_token( email, clave):
    # Definir los datos que se enviarán en la solicitud POST
    data = {
        "email": email,
        "clave": clave
    }

    api_url = 'http://localhost:5000'

    # Hacer la solicitud POST a la ruta de autenticación
    response = requests.post(api_url + '/auth', json=data)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Extraer el token del cuerpo de la respuesta
        token = response.json().get('token')
        print(token)
        return token
    else:
        # Imprimir el mensaje de error si la autenticación falló
        print("Error en la autenticación:", response.json().get('error'))
        return None
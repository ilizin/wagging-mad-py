import requests
import json

def get_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response_json = response.json()
        return response_json

    except requests.exceptions.HTTPError as errh:
        print(f"Error HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error de Conexión: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Error de Tiempo de Espera (Timeout): {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error general en la petición: {err}")
    except ValueError:
        print("La respuesta recibida no es un JSON válido")

    return None

url = "https://datos.madrid.es/dataset/300094-0-areas-caninas/resource/300094-0-areas-caninas/download/300094-0-areas-caninas.json"
response_json = get_data(url)
for elem in response_json:
    print(elem['BARRIO'], elem['DISTRITO'], elem['ESTADO'], elem['TOTAL_ELEM'])
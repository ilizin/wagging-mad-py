import requests
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
import csv

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

def get_data2(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response = response.text
        return response
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
url2 = "https://datos.madrid.es/api/3/action/datastore_search?resource_id=300497-3-distritos-municipales-madrid"
#url = "https://datos.madrid.es/api/3/action/datastore_search?resource_id=300094-0-areas-caninas"
response_json = get_data(url)
response_json2 = get_data(url2)
print(response_json)
print(response_json2)
#spamreader = csv.DictReader(response_csv)
#print(spamreader)
#for row in spamreader:
 #   print(row)
print(f"{'DISTRITO':<25}", f"{'ESTADO':<15}", f"{'TOTAL_ELEM':<15}", f"{'VIA':<15}")
for elem in response_json:
    address = str(elem['TIPO_VIA']) + ' ' + str(elem['NOM_VIA']) + ' ' + str(elem['NUM_VIA'])
    print(f"{elem['DISTRITO']:<25}", f"{elem['ESTADO']:<15}", f"{elem['TOTAL_ELEM']:<15}", f"{address:<15}")
    
print(response_json2['result']['records'])
for elem in response_json2['result']['records']:
    print(f"{elem['NOMBRE']:<25}")
    
console = Console()
console.clear()
title_text = "[bold cyan]WaggingMadPy[/bold cyan]"
centered_title = Align.center(title_text)

# Method B: Using Panel with title_align (Creates a boxed title)
# centered_panel = Panel(title_text, title_align="center", expand=True)

# Print the centered title to the console
console.print(centered_title)

console.print(Panel("Hello, [red]World!"))
console.print(Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you"))

action = inquirer.select(
        message="Search for dog parks:",
        choices=[
            "District",
            "Zip code",
            "Address",
            Separator(),
            Choice(value=None, name="Exit"),
        ],
        default=None,
    ).execute()

if action == "District":
    print(1)

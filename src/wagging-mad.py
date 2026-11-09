import requests
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy import inquirer
from rich import box

import re

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
url2 = "https://datos.madrid.es/api/3/action/datastore_search?resource_id=300497-3-distritos-municipales-madrid"

response_json = get_data(url)
response_json2 = get_data(url2)

#print(f"{'DISTRITO':<25}", f"{'ESTADO':<15}", f"{'TOTAL_ELEM':<15}", f"{'VIA':<15}")
#for elem in response_json:
#    address = str(elem['TIPO_VIA']) + ' ' + str(elem['NOM_VIA']) + ' ' + str(elem['NUM_VIA'])
#    print(f"{elem['DISTRITO']:<25}", f"{elem['ESTADO']:<15}", f"{elem['TOTAL_ELEM']:<15}", f"{address:<15}")
    
#print(response_json2['result']['records'])
districts = {}
for elem in response_json2['result']['records']:
    districts[elem['NOMBRE']] = None
    
console = Console()

title_text = "[bold cyan]WaggingMadPy[/bold cyan]"
centered_panel = Align.center(Panel(title_text,  box.SQUARE, expand=False))

# Method B: Using Panel with title_align (Creates a boxed title)
# centered_panel = Panel(title_text, title_align="center", expand=True)

# Print the centered title to the console

#console.print(Panel("Hello, [red]World!"))
#console.print(Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you"))

search_type_select = inquirer.select(
        message="Search for dog parks in Madrid:",
        choices=[
            Separator(" "),
            "District",
            "Zip code",
            "Address",
            Separator(),
            "About",
            "Exit",
        ],
        default=None,
        long_instruction="ENTER=Confirm, ↑=Up, ↓=Down",
    )
district_in_text = inquirer.text(
            message="Enter a valid Madrid district:",
            completer=districts,
            validate=lambda result: result in districts or result == 'exit',
            invalid_message="The district entered is invalid",
            multicolumn_complete=True,
            long_instruction="ENTER=Confirm, Esc=Home",
        )
postal_code_in_text = inquirer.text(
            message="Enter a valid Madrid postal code:",
            validate=lambda result: re.search("^28[0-9][0-9][0-9]", result) or result == 'exit',
            invalid_message="The postal code entered is invalid",
            multicolumn_complete=True,
            long_instruction="ENTER=Confirm, Esc=Home",
        )

@district_in_text.register_kb("escape")
def _handle_delete(event):
    #choice_name = district_in_text.result_name
    #choice_value= district_in_text.result_value
    # some logic for processing
    # ...
    # skipping the prompt after processing
    district_in_text._mandatory = False
    district_in_text._handle_skip(event)
    # answer the prompt normally after processing
    district_in_text._handle_enter(event)
    
while (True):
    console.clear()
    console.print(centered_panel)
    console.print()
    action = search_type_select.execute()

    if action == "District":
        district = district_in_text.execute()

    if action == 'Zip code':
        posta_code = postal_code_in_text.execute()
        
    if action == 'Exit' or district == 'd':
        break;
        
     
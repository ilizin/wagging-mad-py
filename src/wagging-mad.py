import requests

from prompt_toolkit.filters import is_done
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice, set_title, clear
from prompt_toolkit.styles import Style

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout

from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.formatted_text import HTML

import shutil
import textwrap

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


districts = {}
for elem in response_json2['result']['records']:
    districts[elem['NOMBRE']] = None
    




clear()



# Method B: Using Panel with title_align (Creates a boxed title)
# centered_panel = Panel(title_text, title_align="center", expand=True)

# Print the centered title to the console

#console.print(Panel("Hello, [red]World!"))
#console.print(Panel("Hello, [red]World!", title="Welcome", subtitle="Thank you"))

#while (True):



style = Style.from_dict(
    {
        "frame.border": "#ff4444",
        "selected-option": "bold",
        # ('noreverse' because the default toolbar style uses 'reverse')
        "bottom-toolbar": "#ffffff bg:#333333 noreverse",
    }
)

set_title("WaggingMadPy")

import sys

def set_terminal_size(rows: int, columns: int) -> None:
    # Escape sequence: \x1b[8;{rows};{columns}t
    sys.stdout.write(f"\x1b[8;{rows};{columns}t")
    sys.stdout.flush()

# Set terminal to 30 rows by 100 columns
set_terminal_size(30, 100)
print_formatted_text()
print_formatted_text(HTML('<b> In Madrid, dog areas (áreas caninas or pipicanes) are designated, fenced-in public spaces located</b>'))
print_formatted_text(HTML('<b> within urban parks and green areas where dogs are legally allowed to run, play, and socialize </b>'))
print_formatted_text(HTML('<b> completely off-leash. Maintained by the city council, these enclosures offer a safe environment </b>')) 
print_formatted_text(HTML('<b> away from traffic and general footpaths, helping pet owners integrate their dogs harmoniously into </b>'))
print_formatted_text(HTML('<b> urban life.</b>'))


result = choice(
    message=HTML("<u>Search for dog parks in Madrid:</u>:"),
    options=[
        ("district", "District"),
        ("postal", "Postal code"),
        ("address", "Address"),
        ("about", "About"),
        ("exit", "Exit"),
    ],
    style=style,
    bottom_toolbar=HTML(
        " Press <b>[Up]</b>/<b>[Down]</b> to select, <b>[Enter]</b> to accept."
    ),
    show_frame=True,
)       



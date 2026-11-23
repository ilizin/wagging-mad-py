import requests
import re
import sys

from datetime import date

from rich.text import Text
from rich.console import Console
from rich.table import Table
from rich.align import Align

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice, set_title, clear
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.validation import Validator

def get_data(url):
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.exceptions.HTTPError as errh:
        print(f"Error HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"ConnectionError: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"RequestException: {err}")
    except ValueError:
        print("The response received is not a valid JSON")
    return None

def set_terminal_size(rows: int, columns: int) -> None:
    sys.stdout.write(f"\x1b[8;{rows};{columns}t")
    sys.stdout.flush()
    
dog_parks_url = "https://datos.madrid.es/dataset/300094-0-areas-caninas/resource/300094-0-areas-caninas/download/300094-0-areas-caninas.json"
madrid_districts_url = "https://datos.madrid.es/api/3/action/datastore_search?resource_id=300497-3-distritos-municipales-madrid"
madrid_neighborhood_url = "https://datos.madrid.es/api/3/action/datastore_search?resource_id=300496-4-barrios-madrid"

def threaded_function(arg):
   align = Align('Loading data', align='center',vertical='bottom')
   console.print(align)
   
from threading import Thread

clear()

set_title("WaggingMadPy")
console = Console()
set_terminal_size(40, 100)



thread = Thread(target = threaded_function, args = (10, ))
thread.start()

dog_parks_json = get_data(dog_parks_url)
districts_json = get_data(madrid_districts_url)
neighborhood_json = get_data(madrid_neighborhood_url)

thread.join()

districts = []
districts_code = []
for temp in districts_json['result']['records']:
    districts.append(temp['NOMBRE'])
    districts_code.append(temp['COD_DIS_TX'])
    
neighborhoods = []
neighborhoods_code = []
for temp in neighborhood_json['result']['records']:
    neighborhoods.append(temp['NOMBRE'])
    neighborhoods_code.append(temp['COD_BAR'])

style = Style.from_dict(
    {
        "frame.border": "#ff4444",
        "selected-option": "bold",
        # ('noreverse' because the default toolbar style uses 'reverse')
        "bottom-toolbar": "#ffffff bg:#333333 noreverse",
    }
)



bindings = KeyBindings()

@bindings.add("escape")
def _(event):
    event.app.exit()
    
def draw_table(title, dog_parks_json, console, table_type, answer, code):
    table = Table(title = title)
    if table_type != 'district':
        table.add_column("District", style="cyan", no_wrap=True)
    if table_type != 'neighborhood': 
        table.add_column("Neighborhood", style="cyan", no_wrap=True)
    table.add_column("Address", style="magenta")
    if table_type != 'postal_code':
        table.add_column("Postal code", justify="center", style="green")
    table.add_column("Installation date", style="magenta")
    table.add_column("State", justify="center", style="green")
    for temp in dog_parks_json:
        installationDateMillis = temp['FECHA_INSTALACION']
        installationDateSeconds = installationDateMillis / 1000
        installationDateStr = date.fromtimestamp(installationDateSeconds).strftime("%m/%d/%Y")
        address = temp['TIPO_VIA'].strip() if temp['TIPO_VIA'] != None else ""
        address += temp['NOM_VIA'].strip() if temp['NOM_VIA'] != None else ""
        address += temp['NUM_VIA'].strip() if temp['NUM_VIA'] != None else ""
        
        postal_code = ""
        if table_type != 'postal_code':
            postal_code = temp['COD_POSTAL'].strip() if temp['COD_POSTAL'] != None else ""
        
        if table_type == 'district' and temp['DISTRITO'] != None and temp['COD_DISTRITO'].strip() == code.strip():
            table.add_row(temp['BARRIO'].strip(), address, postal_code, installationDateStr, temp['ESTADO'].strip())        
        if table_type == 'postal_code' and temp['COD_POSTAL'] != None and temp['COD_POSTAL'].strip().lower() == answer.strip().lower():  
            table.add_row(temp['DISTRITO'].strip(), temp['BARRIO'].strip(), address, installationDateStr, temp['ESTADO'].strip())   
        if table_type == 'neighborhood' and temp['BARRIO'] != None and temp['COD_BARRIO'].strip() == code.strip():  
            table.add_row(temp['DISTRITO'].strip(), address, postal_code, installationDateStr, temp['ESTADO'].strip())                        
    align = Align(table,'center')
    console.print(align)

def is_valid_district(text):
    return text.strip() in districts

def is_valid_neighborhood(text):
    return text.strip() in neighborhoods
    
def is_valid_postal_code(text):
    return re.search("^28[0-9][0-9][0-9]", text)
    
district_validator = Validator.from_callable(
    is_valid_district,
    error_message = "The district is not valid",
    move_cursor_to_end = True
)

postal_code_validator = Validator.from_callable(
    is_valid_postal_code,
    error_message = "The postal code is not valid",
    move_cursor_to_end = True
)

neighborhood_validator = Validator.from_callable(
    is_valid_neighborhood,
    error_message = "The neighborhood is not valid",
    move_cursor_to_end = True
)

districts_completer = WordCompleter(districts, ignore_case = True)
neighborhoods_completer = WordCompleter(neighborhoods, ignore_case = True)



while (True):
    clear()

    set_terminal_size(40, 100)
    print_formatted_text()
    print_formatted_text(HTML('<b> In Madrid, dog areas (áreas caninas or pipicanes) are designated, fenced-in public spaces located</b>'))
    print_formatted_text(HTML('<b> within urban parks and green areas where dogs are legally allowed to run, play, and socialize </b>'))
    print_formatted_text(HTML('<b> completely off-leash. Maintained by the city council, these enclosures offer a safe environment </b>')) 
    print_formatted_text(HTML('<b> away from traffic and general footpaths, helping pet owners integrate their dogs harmoniously into </b>'))
    print_formatted_text(HTML('<b> urban life.</b>'))

    result = choice(
        message = HTML("\U0001F436 <u>Search for dog parks in Madrid</u>:"),
        options = [
            ("district", "District"),
            ("neighborhood", "Neighborhood"),
            ("postal", "Postal code"),
            ("address", "Address"),
            ("all", "All"),
            ("about", "About"),
            ("exit", "Exit"),
        ],
        style = style,
        bottom_toolbar = HTML(
            " Press <b>[Up]</b>/<b>[Down]</b> to select, <b>[Enter]</b> to accept."
        ),
        show_frame = True,
    )       

    if result == 'district':
        answer = prompt("Enter a valid Madrid district: ",
            style = style, 
            show_frame = True,
            bottom_toolbar=HTML(
                " Press <b>[Space]</b> to see all the districts, <b>[Up]</b>/<b>[Down]</b> to select, <b>[Enter]</b> to accept, <b>[Esc]</b> to cancel."
            ),
            multiline = False,
            key_bindings = bindings,
            completer = districts_completer,
            validator = district_validator,
            validate_while_typing = False
        )
        if answer != None:
            print();
            index = districts.index(answer.strip())
            draw_table("Dog areas - District:" + answer, dog_parks_json, console, 'district', answer, districts_code[index])   
            input()
            
    if result == 'neighborhood':
        answer = prompt("Enter a valid Madrid neighborhood: ",
            style = style, 
            show_frame = True,
            bottom_toolbar=HTML(
                " Press <b>[Space]</b> to see all the neighborhoods, <b>[Up]</b>/<b>[Down]</b> to select, <b>[Enter]</b> to accept, <b>[Esc]</b> to cancel."
            ),
            multiline = False,
            key_bindings = bindings,
            completer = neighborhoods_completer,
            validator = neighborhood_validator,
            validate_while_typing = False
        )
        if answer != None:
            print();
            index = neighborhoods.index(answer.strip())
            draw_table("Dog areas - Neighborhood:" + answer, dog_parks_json, console, 'neighborhood', answer, neighborhoods_code[index])   
            input()
            
    if result == 'all':
        table = Table(title="Dog areas")
        table.add_column("District", justify="center", style="green")
        table.add_column("Neighborhood", style="cyan", no_wrap=True)
        table.add_column("Address", style="magenta")
        #table.add_column("Installation date", style="magenta")
        table.add_column("State", style="magenta")
        for elem in dog_parks_json:
            dist = elem['DISTRITO'].strip()
            bb = elem['BARRIO'].strip()
            via = elem['TIPO_VIA']
            if via == None:
                via = ""
            else:
                via = via + " " + elem['NOM_VIA'].strip() + " " + elem['NUM_VIA'].strip()
            st = elem['ESTADO']
            if st == None: 
                st = ""
            table.add_row(dist, bb, via, st)
        align = Align(table,'center')
        console.print(align)
                    
        input()
            
    if result == 'postal':
        answer = prompt("Enter a valid Madrid postal code: ",
            style = style, 
            show_frame = True,
            bottom_toolbar = HTML(" Press <b>[Enter]</b> to accept, <b>[Esc]</b> to cancel."),
            multiline = False,
            key_bindings = bindings, 
            validator = postal_code_validator,
            validate_while_typing = False
        )
        if answer != None:
            print();
            draw_table("Dog areas - Postal code:" + answer, dog_parks_json, console, 'postal_code', answer, None)     
            input()
     
    if result == 'exit':
        break;
        
clear()
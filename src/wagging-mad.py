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
    
dog_parks_url = "https://datos.madrid.es/dataset/300094-0-areas-caninas/resource/300094-0-areas-caninas/download/300094-0-areas-caninas.json"
madrid_districts_url = "https://datos.madrid.es/api/3/action/datastore_search?resource_id=300497-3-distritos-municipales-madrid"

dog_parks_json = get_data(dog_parks_url)
districts_json = get_data(madrid_districts_url)

districts = []
districts_code = []
for temp in districts_json['result']['records']:
    districts.append(temp['NOMBRE'])
    districts_code.append(temp['COD_DIS'])

style = Style.from_dict(
    {
        "frame.border": "#ff4444",
        "selected-option": "bold",
        # ('noreverse' because the default toolbar style uses 'reverse')
        "bottom-toolbar": "#ffffff bg:#333333 noreverse",
    }
)

def set_terminal_size(rows: int, columns: int) -> None:
    sys.stdout.write(f"\x1b[8;{rows};{columns}t")
    sys.stdout.flush()

bindings = KeyBindings()

@bindings.add("escape")
def _(event):
    event.app.exit()

def is_valid_district(text):
    return text.strip() in districts
    
def is_valid_postal_code(text):
    return re.search("^28[0-9][0-9][0-9]", text)
    
def draw_table():
    pass
    
district_validator = Validator.from_callable(
    is_valid_district,
    error_message="The district is not valid",
    move_cursor_to_end=True
)

postal_code_validator = Validator.from_callable(
    is_valid_postal_code,
    error_message="The postal code is not valid",
    move_cursor_to_end=True
)

set_title("WaggingMadPy")
districts_completer = WordCompleter(districts)
console = Console()

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
        style=style, 
        show_frame=True,
        bottom_toolbar=HTML(
        " Press <b>[Space]</b> to see all the districts, <b>[Up]</b>/<b>[Down]</b> to select, <b>[Enter]</b> to accept, <b>[Esc]</b> to cancel."
        ),
        multiline=False,
        key_bindings=bindings,
        completer=districts_completer,
        validator=district_validator,
        validate_while_typing=False)
        
        if answer != None:
            print();
            table = Table(title="Dog areas - District:" + answer)
            table.add_column("Neighborhood", style="cyan", no_wrap=True)
            table.add_column("Address", style="magenta")
            table.add_column("Postal code", justify="center", style="green")
            table.add_column("Installation date", style="magenta")
            table.add_column("State", justify="center", style="green")
            #table = Align.center(table, vertical="middle")
            for elem in dog_parks_json:
                a = elem['FECHA_INSTALACION']
                a = a / 1000
                strr = date.fromtimestamp(a).strftime("%m/%d/%Y")
                #print(elem['DISTRITO'])
                if elem['DISTRITO'].strip().lower() == answer.strip().lower():
                    table.add_row(elem['BARRIO'].strip(), elem['TIPO_VIA'].strip() +  " " + elem['NOM_VIA'].strip() + " " + elem['NUM_VIA'].strip(), elem['COD_POSTAL'].strip(), strr, elem['ESTADO'].strip())
                    
            align = Align(table,'center')
            console.print(align)
                    
                    
            input()
            
    if result == 'all':
        table = Table(title="Dog areas")
        table.add_column("District", justify="center", style="green")
        table.add_column("Neighborhood", style="cyan", no_wrap=True)
        table.add_column("Address", style="magenta")
        #table.add_column("Installation date", style="magenta")
        table.add_column("State", style="magenta")
        #table = Align.center(table, vertical="middle")
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
        style=style, 
        show_frame=True,
        bottom_toolbar=HTML(
        " Press <b>[Enter]</b> to accept, <b>[Esc]</b> to cancel."
        ),
        multiline=False,
        key_bindings=bindings, 
        validator=postal_code_validator,
        validate_while_typing=False)
        
        if answer != None:
            print();

            table = Table(title="Dog areas - Postal code:" + answer)
            table.add_column("District", justify="center", style="green")
            table.add_column("Neighborhood", style="cyan", no_wrap=True)
            table.add_column("Address", style="magenta")
            table.add_column("Installation date", style="magenta")
            table.add_column("State", style="magenta")
            #table = Align.center(table, vertical="middle")
            for elem in dog_parks_json:
                a = elem['FECHA_INSTALACION']
                a = a / 1000
                strr = date.fromtimestamp(a).strftime("%m/%d/%Y")
                #print(elem['DISTRITO'])
                if elem['COD_POSTAL'] != None and elem['COD_POSTAL'].strip().lower() == answer.strip().lower():
                    table.add_row(elem['DISTRITO'].strip(), elem['BARRIO'].strip(), elem['TIPO_VIA'].strip() +  " " + elem['NOM_VIA'].strip() + " " + elem['NUM_VIA'].strip(), strr, elem['ESTADO'].strip())
                    
            
            
           
            align = Align(table,'center')
            console.print(align)
                    
            input()
     
    if result == 'exit':
        break;
        
clear()
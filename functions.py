from customtkinter import CTkEntry
from datetime import datetime
import pytz

def is_empty(text: str) -> bool:
    if len(text) <= 0: return True
    return False

def entry_empty(tx: CTkEntry, txt: str):
    if tx.get() == "":
        raise ValueError(f"Campo {txt} vacio")

def find_id(dictionary: dict, search_name: str) -> int | None:
    for id, name in dictionary.items():
        if name == search_name:
            return id
    return None

def is_alphabetic(text: str) -> bool:
    for character in text:
        if not (
            (ord('A') <= ord(character) <= ord('Z')) or
            (ord('a') <= ord(character) <= ord('z')) or
            (ord(character) == ord('á')) or
            (ord(character) == ord('é')) or
            (ord(character) == ord('í')) or
            (ord(character) == ord('ó')) or
            (ord(character) == ord('ú')) or
            (ord(character) == ord('Á')) or
            (ord(character) == ord('É')) or
            (ord(character) == ord('Í')) or
            (ord(character) == ord('Ó')) or
            (ord(character) == ord('Ú')) or
            (ord(character) == ord('ñ')) or
            (ord(character) == ord('Ñ')) or
            (ord(character) == ord(' '))
        ):
            return False
    return True

def clean_str(text: str) -> str:
    return text.lstrip().rstrip()

def get_datetime() -> datetime:
    """Obtener la fecha actual en formato datetime

    :Example:
    >>> get_datetime()
        2024-09-30

    Returns:
        datetime: Fecha actual
    """
    
    return datetime.now().astimezone(pytz.timezone('America/Mexico_City')).date()
# print(get_datetime())

def get_date() -> list[str]:
    """Obtener lista con la fecha actual

    :Example:
    >>> get_date()
        ['2021', '12', '30']

    Returns:
        list: [año, mes, dia]
    """
    
    today = get_datetime()
    return str(today).split('-')
# from utils.utils import check_drive_link, load, save, get_date_from_weekday, read_suspended, write_suspended, is_valid_date_format, SEND_MAIL_PATH, PYTHON_PATH, MAIL_COMMAND, MINUTES_COMMAND, schedule_call, MEETING_DATES_PATH 
from utils.utils import *
import json
import ast
import os
from datetime import date, timedelta, datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import CompleteStyle
from pathlib import Path
from utils.acta_utils import MINUTES_PATH

BASE_DIR = Path(__file__).resolve().parent

HISTORY_PATH = BASE_DIR / "../files/log"

WEEK_MAP = {
    "L": 0,
    "M": 1,
    "X": 2,
    "J": 3,
    "V": 4,
    "S": 5,
    "D": 6,
}

commands = ["help", "exit", "actas", "reus"]

completer = WordCompleter(commands, ignore_case=True)

history = FileHistory(str(HISTORY_PATH))


def actas():
    print("Gestión de actas")
    print("\nSelecciona una órden:")
    print("\t1) Cambiar carpeta donde se guardan las actas")
    print("\t2) Ver dirección actual de la carpeta de actas")
    print("\t3) Volver")
    while True:
        try:
            cmd = input("Selección: ").strip()
            if cmd == "exit":
                break
            elif cmd == "1":
                cambiar_link()
            elif cmd == "2":
                ver_link()
            elif cmd == "3":
                break
            else:
                print("Selecciona una órden válida")
        except KeyboardInterrupt:
            print()
            break

def ver_link():
    with open(str(MINUTES_PATH), "r", encoding="utf-8") as f:
        content = f.read()
    print(content)


def cambiar_link():
    print("Este comando cambia la dirección de la carpeta donde se crearán automáticamente las actas. Debería ser usado sólo una vez al inicio de mandato, al creaar la carpeta de actas del nuevo curso")
    link = input("Introduce el link de la carpeta: ")
    try:
        file_id, exists = check_drive_link(link)
        if exists:
            with open(MINUTES_PATH, "w", encoding="utf-8") as f:
                f.write(link)
            print("Link de la carpeta de actas actualizado con éxito")
        else:
            print("Error: dirección no encontrada o no es una carpeta")
    except ValueError as e:
        print(e)
        print("URL inválida")



def reus():
    print("Gestionar convocatorias de reunión")
    print("Selecciona una órden: ")
    print("\t1) Cambiar día de próxima reu")
    print("\t2) Ver día de próxima reu")
    print("\t3) Suspender convocatorias")
    print("\t4) Volver")

    while True:
        try:
            cmd = input("Selección: ").strip()

            if cmd == "1":
                cambiar_dia_reu()
                break
            elif cmd == "2":
                ver_dia_reu()
                break
            elif cmd == "3":
                gestionar_suspension()
                break
            elif cmd == "4":
                break
            else:
                print("Selecciona una órden válida")
        except KeyboardInterrupt:
            print()
            break


def is_valid_time(s: str) -> bool:
    return bool(re.match(r'^([01]\d|2[0-3]):[0-5]\d$', s))

def get_hour(s: str) -> int:
    return int(s.split(":")[0])

def get_minute(s: str) -> int:
    return int(s.split(":")[1])

def format_time(s):
    if(len(s) == 1)
        return '0' + s
    else:
        return s

def cambiar_dia_reu():
    date_answer = input("Introduce fecha de la próxima reu (DD/MM/YYYY): ")
    hour_answer = input("Introduce la hora (HH:MM): ")

    if  is_valid_date_format(answer) and is_valid_time(hour_answer):
        newdate = datetime.strptime(answer, "%d/%m/%Y").date()
        hour = get_hour(hour_answer)
        minute = get_minute(minute_answer)

        set_last_meeting_date(get_next_meeting_date())
        set_next_meeting_date(newdate)
        set_next_meeting_hour(hour)
        set_next_meeting_minute(minute)

        dia_reu = get_next_meeting_date()
        dia_convocatoria = dia_reu - timedelta(days=5)

        today = date.today()
        sunday = today + timedelta(days=6-today.weekday())


        # El siguiente método:
        # 1. Elimina los cron jobs actuales para mandar correo y crear acta el domingo
        # 2. Crea tareas at para crear el acta y mandar correo el día de la convocatoria
        # 3. Añade los cron jobs para restaurar las reus normales de los viernes (crear acta y mandar correo los domingos a las 19h a partir del siguiente domingo)
        schedule_call(dia_convocatoria, hour, minute)

        print_next_meeting()
    else:
        print("Valor introducido no válido")

def ver_dia_reu():
    print_next_meeting()


def gestionar_suspension():
    suspended = read_suspended()
    if suspended:
        val = "Actualmente las convocatorias están suspendidas. ¿Desea activarlas? (si/no): "
    else:
        val = "Actualmente las convocatorias no están suspendidas. ¿Desea suspenderlas? (si/no)"
    print("Suspender convocatorias")
    answer = input(val)
    if val:
        if answer == "si":
            activar_convocatorias()
    else:
        if answer == "si":
            suspender_convocatorias()

def activar_convocatorias():
        write_suspended(False)
        print("Se han reanudado las convocatorias de reunión")
        print_next_meeting()

def suspender_convocatorias():
        write_suspended(True)
        print("Se han suspendido las convocatorias de reunión")

def print_next_meeting():
        proxima_reu = get_next_meeting_date()
        proxima_conv = proxima_reu - timedelta(days=5)
        print(f"La próxima reunión será el {proxima_reu.strftime('%d/%m/%Y')}. Se ha programado la convocatoria para el {proxima_conv.strftime('%d/%m/%Y')} a las {format_time(get_next_meeting_hour)}:{format_time(get_next_meeting_minute)}")

def main():
    while True:
        try:
            cmd = prompt("secre > ", 
                         history=history, 
                         completer=completer,
                         complete_while_typing=False,
                         complete_style=CompleteStyle.READLINE_LIKE)

            if cmd == "exit":
                break

            elif cmd == "help":
                print("Comandos:")
                print("\t- reus\tModificar fecha de próximas reus")
                print("\t- actas\tCambiar carpeta de actas")
                print("\t- exit\tSalir")
                break
            elif cmd == "":
                continue
            elif cmd == "actas":
                actas()
            elif cmd == "reus":
                reus()

            else:
                print(f"Comando desconocido: {cmd}")

        except KeyboardInterrupt:
            print()
            break

if __name__ == "__main__":
    main()

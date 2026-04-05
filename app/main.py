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
    print("\nGestión de actas")
    print("Selecciona una órden:")
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
    content = load_from_file(MINUTES_PATH)
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
    print("\nGestionar reuniones")
    print("Selecciona una órden: ")
    print("\t1) Cambiar día de próxima reu")
    print("\t2) Ver día de próxima reu")
    print("\t3) Suspender convocatorias")
    print("\t4) Ver puntos de reunión")
    print("\t5) Modificar puntos de reunión")
    print("\t6) Volver")

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
                ver_puntos()
                break
            elif cmd == "5":
                modificar_puntos()
                break
            elif cmd == "6":
                break
            else:
                print("Selecciona una órden válida")
        except KeyboardInterrupt:
            print()
            break

def ver_puntos():
    print("\nVer puntos")
    print("Selecciona una órden: ")
    print("1) Ver puntos permanentes")
    print("2) Ver puntos temporales (si hay)")

    ans = input("\nSelección: ")

    if ans == "1":
        day = load_from_json(DAY_POINTS_PATH)
        night = load_from_json(NIGHT_POINTS_PATH)
        print("PUNTOS DEL DÍA")
        for item in day:
            print('\t'+item)

        print("PUNTOS DE NOCHE")
        for item in night:
            print('\t'+item)
    elif ans == "2":
        if does_file_exist(DAY_POINTS_TEMP_PATH):
            day_temp = load_from_json(DAY_POINTS_TEMP_PATH)
            print("PUNTOS DEL DÍA (Temporales)")
            for item in day_temp:
                print('\t'+item)
        else:
            day = load_from_json(DAY_POINTS_PATH)
            print("PUNTOS DEL DÍA (Permanentes)")
            for item in day:
                print('\t'+item)
        if does_file_exist(NIGHT_POINTS_TEMP_PATH):
            night_temp = load_from_json(NIGHT_POINTS_TEMP_PATH)
            print("PUNTOS DE NOCHE (Temporales)")
            for item in night_temp:
                print('\t'+item)
        else:
            night = load_from_json(NIGHT_POINTS_PATH)
            print("PUNTOS DE NOCHE (Permanentes)")
            for item in night:
                print('\t'+item)


def modificar_puntos():
    print("Modificar puntos")
    print("Selecciona una orden:")
    print("1) Modificar puntos del día")
    print("2) Modificar puntos de noche")
    print()
    cmd = input("Selección: ").strip()

    if cmd == "1":
        print("Introduce los puntos del día (o nada para finalizar): ")
        items = []
        while True:
            item = input("Añadir punto: ")
            if item == "":
                break
            items.append(item)
        save_into_json(items, DAY_POINTS_PATH)
        ans = input("¿Deseas actualizarlos de manera temporal o permanente? Si escribes 'temporal', sólo se modificarán para la próxima reu. Si eliges 'permanente', se convertirán en los puntos por defecto (temporal/permanente): ")
        if ans == "temporal":
            if not does_file_exist(DAY_POINTS_TEMP_PATH):
                save_into_json(items, DAY_POINTS_TEMP_PATH)
            print("Puntos del día actualizados para la próxima reu")
        elif ans == "permanente":
            save_into_json(items, DAY_POINTS_PATH)
            print("Puntos del día actualizados")
        else:
            print("Comando inválido. Operación abortada.")
    elif cmd == "2":
        print("Introduce los puntos de noche (o nada para finalizar): ")
        items = []
        while True:
            item = input("Añadir punto: ")
            if item == "":
                break
            items.append(item)
        ans = input("¿Deseas actualizarlos de manera temporal o permanente? Si escribes 'temporal', sólo se modificarán para la próxima reu. Si eliges 'permanente', se convertirán en los puntos por defecto (temporal/permanente): ")
        if ans == "temporal":
            if not does_file_exist(NIGHT_POINTS_TEMP_PATH):
                create_file(NIGHT_POINTS_TEMP_PATH)
            save_into_json(items, NIGHT_POINTS_TEMP_PATH)
            print("Puntos de noche actualizados para la próxima reu")
        elif ans == "permanente":
            save_into_json(items, NIGHT_POINTS_PATH)
            print("Puntos de noche actualizados")
        else:
            print("Comando inválido. Operación abortada.")
    else:
        print("Selección inválida")




def is_valid_time(s: str) -> bool:
    return bool(re.match(r'^([01]\d|2[0-3]):[0-5]\d$', s))

def get_hour(s: str) -> int:
    return int(s.split(":")[0])

def get_minute(s: str) -> int:
    return int(s.split(":")[1])


def cambiar_dia_reu():
    date_answer = input("Introduce fecha de la próxima reu (DD/MM/YYYY): ")
    hour_answer = input("Introduce la hora (HH:MM): ")

    if  is_valid_date_format(date_answer) and is_valid_time(hour_answer):
        newdate = datetime.strptime(date_answer, "%d/%m/%Y").date()
        hour = get_hour(hour_answer)
        minute = get_minute(hour_answer)

        set_last_meeting_date(get_next_meeting_date())
        set_next_meeting_date(newdate)
        set_next_meeting_hour(hour)
        set_next_meeting_minute(minute)

        dia_convocatoria = get_call_date()

        # El siguiente método:
        # 1. Elimina los cron jobs actuales para mandar correo y crear acta el domingo
        # 2. Crea tareas at para crear el acta y mandar correo el día de la convocatoria
        # 3. Añade los cron jobs para restaurar las reus normales de los viernes (crear acta y mandar correo los domingos a las 19h a partir del siguiente domingo)
        schedule_call(dia_convocatoria, hour, minute)

        print_next_meeting()
    else:
        print("Valor introducido no válido. Operación abortada")

def ver_dia_reu():
    suspended = read_suspended()
    if suspended:
        print("Las convocatorias están suspendidas. Actívalas para ver la fecha de la próxima reunión")
    else:
        print_next_meeting()


def gestionar_suspension():
    suspended = read_suspended()
    if suspended:
        val = "Actualmente las convocatorias están suspendidas. ¿Desea activarlas? (si/no): "
    else:
        val = "Actualmente las convocatorias no están suspendidas. ¿Desea suspenderlas? (si/no): "
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
        schedule_call(get_next_meeting_date(), get_next_meeting_hour(), get_next_meeting_minute())
        print_next_meeting()

def suspender_convocatorias():
        borrar_scheduled_jobs()
        write_suspended(True)
        print("Se han suspendido las convocatorias de reunión")

def print_next_meeting():
        proxima_reu = get_next_meeting_date()
        proxima_conv = get_call_date()
        print(f"La próxima reunión será el {proxima_reu.strftime('%d/%m/%Y')}. Se ha programado la convocatoria para el {proxima_conv.strftime('%d/%m/%Y')} a las {format_time(str(get_next_meeting_hour()))}:{format_time(str(get_next_meeting_minute()))}")

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

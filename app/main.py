from utils.utils import check_drive_link, load, save, get_date_from_weekday, read_suspended, write_suspended
import json
import ast
import os
from utils.utils import get_date_from_weekday
from datetime import date, timedelta
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import CompleteStyle
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

HISTORY_PATH = BASE_DIR / "../files/log"
MINUTES_PATH = BASE_DIR / "../files/minutes_id"
MEETING_DATES_PATH = BASE_DIR / "../files/meeting_dates"

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
            elif cmd == "2":
                ver_dia_reu()
            elif cmd == "3":
                suspender_convocatorias()
                break
            elif cmd == "4":
                break
            else:
                print("Selecciona una órden válida")
        except KeyboardInterrupt:
            print()
            break



def cambiar_dia_reu():
    weekday = input("Introduce el día de la semana de la próxima reu (L, M, X, J, V, S, D): ")

    newdate = get_date_from_weekday(weekday)

    data = load(MEETING_DATES_PATH)

    # update second position
    data[1] = newdate.isoformat()

    # write back
    save(MEETING_DATES_PATH, data)

    dia_convocatoria = date.fromisoformat(data[1]) - timedelta(days=5)
    print(f"La próxima reunión será el {newdate.strftime('%d/%m/%Y')}. La convocatoria está programada para el {dia_convocatoria} a las 19:00")

def ver_dia_reu():
    data = load(MEETING_DATES_PATH)

    second_date = date.fromisoformat(data[1])
    dia_convocatoria = date.fromisoformat(data[1]) - timedelta(days=5)
    print(f"La próxima reunión será el {second_date.strftime('%d/%m/%Y')}. La convocatoria está programada para el {dia_convocatoria} a las 19:00")


def suspender_convocatorias():
    suspended = read_suspended()
    print("Suspender convocatorias: introduce el número de semanas para las que se suspenden las reuniones, o escribe S para suspenderlas indefinidamente")
    while True:
        resp = input("Introduce respuesta: ")
        if resp.isdigit():
            # Suspender convocatorias X semanas
            data = load(MEETING_DATES_PATH)

            second_date = date.fromisoformat(data[1])
            lunes1 = second_date - timedelta(days=second_date.weekday())

            tmp = second_date + timedelta(weeks=int(resp))
            lunes2 = tmp - timedelta(days=tmp.weekday())

            proxima_reu = lunes2 + timedelta(days=second_date.weekday())

            proxima_conv = proxima_reu - timedelta(days=5)

            data[1] = date.isoformat(proxima_conv)

            save(MEETING_DATES_PATH, data)
            print(f"La próxima reunión será el {proxima_reu.strftime('%d/%m/%Y')}. Se ha programado la convocatoria para el {proxima_conv.strftime('%d/%m/%Y')} a lass 19:00")
            break
        elif resp == 'S':
            if suspended:
                data = load(MEETING_DATES_PATH)
                proxima_reu = date.fromisoformat(data[1])
                proxima_conv = proxima_reu - timedelta(days=5)
                write_suspended(False)
                print("Se han reanudado las convocatorias de reunión")
                print(f"La próxima reunión será el {proxima_reu.strftime('%d/%m/%Y')}. Se ha programado la convocatoria para el {proxima_conv.strftime('%d/%m/%Y')} a lass 19:00")
            else:
                write_suspended(True)
                print("Se han suspendido las convocatorias indefinidamente. Vuelve a ejecutar el comando para activarlas.")
            break
        else:
            print("Introduce una respuesta válida")

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
                print("Available commands: help, exit")

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

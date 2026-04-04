from utils import check_drive_link





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
    with open("../files/minutes_id", "r", encoding="utf-8") as f:
        content = f.read()
    print(content)


def cambiar_link():
    print("Este comando cambia la dirección de la carpeta donde se crearán automáticamente las actas. Debería ser usado sólo una vez al inicio de mandato, al creaar la carpeta de actas del nuevo curso")
    link = input("Introduce el link de la carpeta: ")
    try:
        file_id, exists = check_drive_link(link)
        if exists:
            with open("../files/minutes_id", "w", encoding="utf-8") as f:
                f.write(link)
            print("Link de la carpeta de actas actualizado con éxito")
        else:
            print("Error: dirección no encontrada o no es una carpeta")
    except ValueError as e:
        print(e)
        print("URL inválida")

def main():
    while True:
        try:
            cmd = input("secre > ").strip()

            if cmd == "exit":
                break

            elif cmd == "help":
                print("Available commands: help, exit")

            elif cmd == "":
                continue
            elif cmd == "actas":
                actas()

            else:
                print(f"Comando desconocido: {cmd}")

        except KeyboardInterrupt:
            print()
            break

if __name__ == "__main__":
    main()

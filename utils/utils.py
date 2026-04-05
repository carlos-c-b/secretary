import re
import subprocess
from datetime import datetime, date, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
TOKEN_PATH = BASE_DIR / "../token.json"
PYTHON_PATH = BASE_DIR / "../venv/bin/python"
SUSPENDED_PATH = BASE_DIR / "../files/suspended"
SEND_MAIL_PATH = BASE_DIR / "mails.mail-convocatora-reu"
CREATE_MINUTES_PATH = BASE_DIR / "utils.acta_utils"
CRON_PATH = BASE_DIR / "utils.cron"
MEETING_DATES_PATH = BASE_DIR / "../files/meeting_dates"
DAY_POINTS_PATH = BASE_DIR / "../files/day_points"
NIGHT_POINTS_PATH = BASE_DIR / "../files/night_points"
DAY_POINTS_TEMP_PATH = BASE_DIR / "../files/day_points_temp"
NIGHT_POINTS_TEMP_PATH = BASE_DIR / "../files/night_points_temp"

MAIL_COMMAND = f"{PYTHON_PATH} -m {SEND_MAIL_PATH}"
MINUTES_COMMAND = f"{PYTHON_PATH} -m {CREATE_MINUTES_PATH}"
CRON_COMMAND = f"{PYTHON_PATH} -m {CRON_PATH}"






SCOPES = ["https://www.googleapis.com/auth/drive"]

WEEK_MAP = {
    "L": 0,
    "M": 1,
    "X": 2,
    "J": 3,
    "V": 4,
    "S": 5,
    "D": 6,
}

def extract_file_id(url: str) -> str:
   
    match = re.search(r"drive\.google\.com/drive/(?:u/\d+/)?folders/([a-zA-Z0-9_-]+)", url)
    if not match:
        raise ValueError("Link inválido")
    return match.group(1)


def create_file(path):
    Path(path).touch()

def does_file_exist(path):
    p = Path(path)
    return p.exists()

def delete_file(path):
    Path(path).unlink()


def save_into_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def folder_exists(file_id: str, service) -> bool:
    try:
        file = service.files().get(
                fileId=file_id,
                fields="id, mimeType",
                supportsAllDrives=True
                ).execute()
        return file["mimeType"] == "application/vnd.google-apps.folder"
    except Exception as e:
        print(e)
        return False


def check_drive_link(url: str):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    service = build("drive", "v3", credentials=creds)

    file_id = extract_file_id(url)
    exists = folder_exists(file_id, service)

    return file_id, exists


def get_date_from_weekday(letter: str) -> date:
    letter = letter.upper()

    if letter not in WEEK_MAP:
        raise ValueError("Día de semana inválido. Usa L, M, X, J, V, S, D")

    today = date.today()

    # Monday of current week
    monday = today - timedelta(days=today.weekday())

    target_date = monday + timedelta(days=WEEK_MAP[letter])

    return target_date

def load(file_path):
    with open(file_path) as f:
        return json.load(f)

def save(file_path, data):
    clean = [
            x.isoformat() if isinstance(x,date) else x
            for x in data
            ]
    with open(file_path, "w") as f:
        json.dump(data, f)

# Devuelve True si el archivo contiene "Suspendido" y False en otro caso
def read_suspended():
    with open(SUSPENDED_PATH, "r", encoding="utf-8") as f:
        data = f.read()
    if data == "Suspendido":
        return True
    else:
        return False

def write_suspended(boolean_val):
    if boolean_val:
        data = "Suspendido"
    else:
        data = "No suspendido"
    with open(SUSPENDED_PATH, "w", encoding="utf-8") as f:
        f.write(data)

def is_valid_date_format(s: str) -> bool:
    try:
        datetime.strptime(s, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def schedule_weekly_safe(date_obj, hour, minute, command):
    weekday = (date_obj.weekday() + 1) % 7
    cron_line = f"{minute} {hour} * * {weekday} {command}"

    result = subprocess.run("crontab -l 2>/dev/null", shell=True, capture_output=True, text=True)
    existing = result.stdout

    if cron_line not in existing:
        new_cron = existing + cron_line + "\n"
        subprocess.run("crontab -", input=new_cron, text=True, shell=True)


def get_last_meeting_date():
    data = load(MEETING_DATES_PATH)
    return date.fromisoformat(data[0])

def get_next_meeting_date():
    data = load(MEETING_DATES_PATH)
    return date.fromisoformat(data[1])

def get_next_meeting_hour():
    data = load(MEETING_DATES_PATH)
    return data[2]

def get_next_meeting_minute():
    data = load(MEETING_DATES_PATH)
    return data[3]

def set_last_meeting_date(date):
    data = load(MEETING_DATES_PATH)
    data[0] = date.isoformat()
    save(MEETING_DATES_PATH, data)

def set_next_meeting_date(date):
    data = load(MEETING_DATES_PATH)
    data[1] = date.isoformat()
    save(MEETING_DATES_PATH, data)

def set_next_meeting_hour(hour):
    data = load(MEETING_DATES_PATH)
    data[2] = hour
    save(MEETING_DATES_PATH, data)
def set_next_meeting_minute(minute):
    data = load(MEETING_DATES_PATH)
    data[3] = minute
    save(MEETING_DATES_PATH, data)

def remove_cron_job(command):
    # Get current crontab
    result = subprocess.run(
        "crontab -l 2>/dev/null",
        shell=True,
        capture_output=True,
        text=True
    )
    
    lines = result.stdout.splitlines()

    # Keep only lines that DO NOT contain the command
    new_lines = [line for line in lines if command not in line]

    # Write back new crontab
    new_cron = "\n".join(new_lines) + "\n"

    subprocess.run(
        "crontab -",
        input=new_cron,
        text=True,
        shell=True
    )

def format_time(s):
    if(len(s) == 1):
        return '0' + s
    else:
        return s

def clear_all_at_jobs():
    result = subprocess.run("atq", shell=True, capture_output=True, text=True)
    job_ids = [line.split()[0] for line in result.stdout.splitlines()]

    for job_id in job_ids:
        subprocess.run(f"atrm {job_id}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)



def schedule_job(date_obj, hour, minute, command):
    time_str = f"{date_obj:%Y%m%d}{int(hour):02d}{int(minute):02d}"
    at_command = f'echo "{MINUTES_COMMAND}" | at -t {time_str}'
    subprocess.run(at_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_call_date():
    dia_reu = get_next_meeting_date()
    return dia_reu - timedelta(days=5)

def borrar_scheduled_jobs():
    # Borramos los cron jobs actuales para el acta y el correo
    remove_cron_job(MAIL_COMMAND)
    remove_cron_job(MINUTES_COMMAND)

    # Borramos los at actuales
    clear_all_at_jobs()

def schedule_call(date_obj, hour, minute):
    borrar_scheduled_jobs()

    # Programamos el at para crear el acta
    if(minute == 0):
        hour_acta = hour-1
        minute_acta = 59
    else:
        hour_acta = hour
        minute_acta = minute-1
    schedule_job(date_obj, hour_acta, minute_acta, MINUTES_COMMAND)

    # Restauramos los cron jobs para el acta y la convocatoria normal a partir del siguiente domingo a las 19
    date_obj += timedelta(days=7)
    schedule_job(date_obj, 18, 0, CRON_COMMAND)
    print("A partir de la siguiente semana, las convocatorias se mandarán el domingo a las 19:00")

    print(f"Se creará el acta el {date_obj.strftime('%d/%m/%Y')} a las {format_time(str(hour_acta))}:{format_time(str(minute_acta))}")
    # Programamos el at para mandar este correo
    schedule_job(date_obj, hour, minute, MAIL_COMMAND)
    print(f"Se mandará el correo el {date_obj.strftime('%d/%m/%Y')} a las {format_time(str(hour))}:{format_time(str(minute))}")


# Función de debuggear para enviar correo instantaneamnete y crear el acta
def send_instantly():
    borrar_scheduled_jobs()
    

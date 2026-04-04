import re
from datetime import date, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
TOKEN_PATH = BASE_DIR / "../token.json"
SUSPENDED_PATH = BASE_DIR / "../files/suspended"


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



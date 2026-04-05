import json
import os
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from utils.utils import extract_file_id
from pathlib import Path

# ----------------------------
# CONFIG
# ----------------------------

SCOPES = ["https://www.googleapis.com/auth/drive"]


TEMPLATE_ID = "1nRL0RDUWwyGiGEPeAcBk-wW3dlKMr9YGJhIMGwghfSU"

BASE_DIR = Path(__file__).resolve().parent
MINUTES_PATH = BASE_DIR / "../files/minutes_folder_id"
LAST_MINUTES_ID = BASE_DIR / "../files/last_minutes_id"

with open(MINUTES_PATH, "r", encoding="utf-8") as f:
    PARENT_FOLDER_ID = extract_file_id(f.read())


MONTHS = {
   1: "Septiembre",
    2: "Octubre",
    3: "Noviembre",
    4: "Diciembre",
    5: "Enero",
    6: "Febrero",
    7: "Marzo",
    8: "Abril",
    9: "Mayo",
    10: "Junio",
    11: "Julio",
    12: "Agosto",
}


def get_folder_by_name(service, name, parent_id):
    query = (
        f"mimeType='application/vnd.google-apps.folder' "
        f"and name='{name}' "
        f"and '{parent_id}' in parents "
        f"and trashed=false"
    )

    results = service.files().list(
        q=query,
        fields="files(id, name)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    ).execute()

    files = results.get("files", [])

    return files[0]["id"] if files else None

# ----------------------------
# LOAD / SAVE CACHE
# ----------------------------

def load_folder_ids():
    if not os.path.exists(FOLDER_DB):
        return {}
    with open(FOLDER_DB, "r") as f:
        return json.load(f)


def save_folder_ids(data):
    with open(FOLDER_DB, "w") as f:
        json.dump(data, f, indent=2)


# ----------------------------
# DRIVE SETUP
# ----------------------------

def get_service():
    creds = Credentials.from_authorized_user_file("../token.json", SCOPES)
    return build("drive", "v3", credentials=creds)


# ----------------------------
# CORE LOGIC
# ----------------------------

def get_or_create_folder(service, name, parent_id):
    folder_id = get_folder_by_name(service, name, parent_id)

    if folder_id:
        return folder_id

    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }

    folder = service.files().create(
        body=metadata,
        fields="id",
        supportsAllDrives=True
    ).execute()

    return folder["id"]

def copy_template(service, folder_id):
    body = {
        "name": f"Acta de reunión {datetime.now().strftime('%d/%m/%Y')}",
        "parents": [folder_id],
    }

    return service.files().copy(
        fileId=TEMPLATE_ID,
        body=body,
        supportsAllDrives=True
    ).execute()

def academic_month_index(real_month: int) -> int:
    return ((real_month - 9) % 12) + 1


def save_file_id(file_id):
    with open(LAST_MINUTES_PATH, "w", encoding="utf-8") as f:
        f.write(file_id)

def get_last_minutes_id():
    with open(LAST_MINUTES_PATH, "r", encoding="utf-8") as f:
        return f.read()

def create_new_minutes():
    service = get_service()


    now = datetime.now()
    index = academic_month_index(now.month)
    folder_name = f"{index}. {MONTHS[index]}"

    folder_id = get_or_create_folder(service, folder_name, PARENT_FOLDER_ID)
    file = copy_template(service, folder_id)
    save_file_id(file)  # Guardamos el id del acta recién creada
    return file

def main():
    last_minutes_id = get_last_minutes_id()
    new_minutes_id = create_new_minutes()

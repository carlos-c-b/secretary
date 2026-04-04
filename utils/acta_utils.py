import json
import os
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# ----------------------------
# CONFIG
# ----------------------------

SCOPES = ["https://www.googleapis.com/auth/drive"]
FOLDER_DB = "folder_ids.json"

TEMPLATE_ID = "1nRL0RDUWwyGiGEPeAcBk-wW3dlKMr9YGJhIMGwghfSU"
PARENT_FOLDER_ID = "1MfMJpwuYrUekiCb1_fEl0wVT3oBlbV3r"

MONTHS = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}


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

def get_or_create_month_folder(service, month_name, cache):
    if month_name in cache:
        return cache[month_name]

    # Create folder in Drive
    folder_metadata = {
        "name": month_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [PARENT_FOLDER_ID],
    }

    folder = service.files().create(body=folder_metadata, fields="id", supportsAllDrives=True).execute()
    folder_id = folder["id"]

    cache[month_name] = folder_id
    save_folder_ids(cache)

    return folder_id


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


# ----------------------------
# MAIN
# ----------------------------

def main():
    service = get_service()
    cache = load_folder_ids()


    now = datetime.now()
    month_name = f"{now.month}. {MONTHS[now.month]}"

    folder_id = get_or_create_month_folder(service, month_name, cache)
    file = copy_template(service, folder_id)

    print("Created file:", file["id"])
    print("In folder:", folder_id)


if __name__ == "__main__":
    main()


import re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/drive"]

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
    creds = Credentials.from_authorized_user_file("../token.json", SCOPES)
    service = build("drive", "v3", credentials=creds)

    file_id = extract_file_id(url)
    exists = folder_exists(file_id, service)

    return file_id, exists


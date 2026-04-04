from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os

SCOPES = ["https://www.googleapis.com/auth/drive"]

# Authenticate
def authenticate():
    creds = None
    path_tok = "../token.json"

    if os.path.exists(path_tok):
        creds = Credentials.from_authorized_user_file(path_tok, SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "../credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(path_tok, "w") as token:
            token.write(creds.to_json())

    return creds

# Main logic
def copy_template():
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    TEMPLATE_ID = "1nRL0RDUWwyGiGEPeAcBk-wW3dlKMr9YGJhIMGwghfSU"
    FOLDER_ID = "1kCEusFVuG9QpP7JymZ8M-xip2UvfRYZY"

    today = datetime.datetime.now().strftime("%d/%m/%y")

    new_file_metadata = {
        "name": f"Acta de reunión {today}",
        "parents": [FOLDER_ID]
    }

    file = service.files().copy(
        fileId=TEMPLATE_ID,
        body=new_file_metadata,
        supportsAllDrives=True
    ).execute()

    print("Created file ID:", file.get("id"))


if __name__ == "__main__":
    copy_template()

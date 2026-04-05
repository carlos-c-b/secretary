from .utils import TOKEN_PATH
from googleapiclient.discovery import build

SCOPES = [
    # ... your existing scopes
    "https://www.googleapis.com/auth/gmail.send"
]


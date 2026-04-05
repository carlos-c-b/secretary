import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os
from jinja2 import Template
from pathlib import Path
from utils.acta_utils import last_minutes_id, new_minutes_id

BASE_DIR = Path(__file__).resolve().parent
MAIL_PATH = BASE_DIR / "../mails/convocatoria-reu.html"

# Dates
today = datetime.now()
yesterday = today - timedelta(days=1)
week_ago = today - timedelta(days=7)


today_str = today.strftime("%d/%m/%Y")
yesterday_str = yesterday.strftime("%d/%m")
week_ago_str = week_ago.strftime("%d/%m/%Y")

days_es = [
    "lunes", "martes", "miércoles", "jueves",
    "viernes", "sábado", "domingo"
]

# Spanish months
months_es = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

date = datetime.now()

day = date.day
month = months_es[date.month - 1]

def format_spanish_date(date_str):
    date = datetime.strptime(date_str, "%d/%m/%Y")

    day_name = days_es[date.weekday()].upper()
    day_num = date.day
    month_name = months_es[date.month - 1]

    return f"{day_name} {day_num} de {month_name}"

today_formatted = format_spanish_date(today_str)


with open(MAIL_PATH, "r", encoding="utf-8") as f:
    template = Template(f.read())

last_minutes_link = f"https://docs.google.com/document/d/{last_minutes_id}/edit"
new_minutes_link = f"https://docs.google.com/document/d/{new_minutes_id}/edit"

html = template.render(
    today_str = today_str,
    yesterday_str=yesterday_str,
    week_ago_str=week_ago_str,
    today_formatted=today_formatted
    last_minutes_link=last_minutes_link
    new_minutes_link=new_minutes_link
)


# Email content
subject = "Test Email"

msg = MIMEText(html, "html")
msg["Subject"] = subject
msg["From"] = "secretary@bestvalencia.org"
msg["To"] = "carloscbc2004@gmail.com"

# SMTP server (example: Gmail)
smtp_server = "smtp.gmail.com"
smtp_port = 465

username = "secretary@bestvalencia.org"
password = os.getenv("EMAIL_PASSWORD") # use app password, not your real password

# Send email
with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
    server.login(username, password)
    server.send_message(msg)

print("Email sent!")

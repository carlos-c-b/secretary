import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import os
from jinja2 import Template



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


with open("convocatoria-reu.html", "r", encoding="utf-8") as f:
    template = Template(f.read())

html = template.render(
    today_str = today_str,
    yesterday_str=yesterday_str,
    week_ago_str=week_ago_str,
    today_formatted=today_formatted
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

import smtplib
import os
from email.mime.text import MIMEText

# Email content
subject = "Test Email"
body = "Hello, this is a simple automated email from Python."

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = "carlos.beltran@bestvalencia.org"
msg["To"] = "carloscbc2004@gmail.com"

# SMTP server (example: Gmail)
smtp_server = "smtp.gmail.com"
smtp_port = 465

username = "carlos.beltran@bestvalencia.org"
password = os.getnev("EMAIL_PASSWORD") # use app password, not your real password

# Send email
with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
    server.login(username, password)
    server.send_message(msg)

print("Email sent!")

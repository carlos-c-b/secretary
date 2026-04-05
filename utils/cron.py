from utils.utils import schedule_weekly_safe, MAIL_COMMAND, MINUTES_COMMAND

# Crea los cron jobs para crear el acta y mandar el correo los domingos a las 19h. Debe llamarse con un at desde la función schedule_call en utils.py
def main():
    today = date.today()
    schedule_weekly_safe(today, 18, 59, MINUTES_COMMAND)
    schedule_weekly_safe(today, 19, 0, MINUTES_COMMAND)

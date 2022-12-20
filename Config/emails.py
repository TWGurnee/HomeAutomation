import smtplib
from email.mime.text import MIMEText
from Config.config import SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT, SMTP_EMAIL

# Defines helper email functions for reminders.

def send_email(subject: str, msg: str, send_to: str):
    # Convert text to gmail format
    msg = MIMEText(msg)

    # Grab email-address from config and assign
    msg['To'] = send_to
    msg['From'] = SMTP_EMAIL
    msg['Subject'] = subject

    # Send email
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
    smtp.sendmail(SMTP_EMAIL, send_to, msg.as_string())
    print(f'Sent {subject} email to: {send_to}')
    smtp.quit()
import smtplib
from email.mime.text import MIMEText
from Config.config import SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT, EMAIL

# Defines helper email functions for reminders.

def send_email(subject: str, msg: str):
    # Convert text to gmail format
    msg = MIMEText(msg)

    # Grab email-address from config and assign
    msg['To'] = EMAIL
    msg['From'] = EMAIL
    msg['Subject'] = subject

    # Send email
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(EMAIL, SMTP_PASSWORD)
    smtp.sendmail(EMAIL, EMAIL, msg.as_string())
    print(f'Sent {subject} email to: {EMAIL}')
    smtp.quit()
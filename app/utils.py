import smtplib
from email.message import EmailMessage

from app.config import Config


def send_email(subject: str, body: str, to: str | None = None) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = Config.SMTP_USERNAME or "noreply@example.com"
    msg["To"] = to or Config.NOTIFY_EMAIL or "admin@example.com"
    msg.set_content(body)

    server = smtplib.SMTP(str(Config.SMTP_SERVER), int(Config.SMTP_PORT))
    server.starttls()
    server.login(
        str(Config.SMTP_USERNAME),
        str(Config.SMTP_PASSWORD),
    )
    server.send_message(msg)
    server.quit()

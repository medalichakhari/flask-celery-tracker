import os


class Config:
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.example.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "noreply@example.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "changeme123")
    NOTIFY_EMAIL: str = os.getenv("NOTIFY_EMAIL", "admin@example.com")

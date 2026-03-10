import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL")

def send_discord(message: str) -> None:
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("Discord értesítés elküldve! ✅")
    else:
        print(f"Discord hiba: {response.status_code}")

def send_email(subject: str, message: str) -> None:
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = NOTIFY_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, NOTIFY_EMAIL, msg.as_string())
        print("Email elküldve! ✅")

def notify(game_name: str, original_price: float, current_price: float, discount: int) -> None:
    message = (
        f"🎮 AKCIÓ: {game_name}\n"
        f"💰 Eredeti ár: {original_price}€\n"
        f"🔥 Jelenlegi ár: {current_price}€\n"
        f"📉 Kedvezmény: {discount}%"
    )
    send_discord(message)
    send_email(f"Steam akció: {game_name}", message)

if __name__ == "__main__":
    notify("Satisfactory", 38.99, 27.29, 30)
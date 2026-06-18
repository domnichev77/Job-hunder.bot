import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

r = requests.get(
    "https://api.hh.ru/suggests/areas",
    params={
        "text": "Усть-Каменогорск"
    },
    headers={
        "User-Agent": "JobHunterBot/1.0"
    }
)

msg = r.text[:3500]

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": msg
    }
)

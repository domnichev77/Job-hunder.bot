import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

response = requests.get(
    "https://api.hh.ru/vacancies",
    params={
        "area": 160,
        "page": 0,
        "per_page": 20
    },
    headers={
        "User-Agent": "JobHunterBot/1.0"
    }
)

text = response.text[:3000]

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": text
    }
)

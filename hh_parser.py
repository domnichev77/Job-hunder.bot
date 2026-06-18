import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
}

r = requests.get(
    "https://api.hh.ru/vacancies",
    params={
        "area": 194,
        "per_page": 10,
        "page": 0
    },
    headers=headers
)

msg = (
    f"status={r.status_code}\n\n"
    f"headers={r.headers}\n\n"
    f"{r.text[:3000]}"
)

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": msg[:4000]
    }
)

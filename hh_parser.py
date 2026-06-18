import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

headers = {
    "User-Agent": "JobHunterBot/1.0 (contact: your_email@example.com)",
    "Accept": "application/json"
}

r = requests.get(
    "https://api.hh.ru/vacancies",
    params={
        "area": 194,
        "per_page": 10,
        "page": 0
    },
    headers=headers,
    timeout=20
)

msg = f"status={r.status_code}\n\n{r.text[:3000]}"

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": msg
    }
)

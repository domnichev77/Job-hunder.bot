import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

html = requests.get(
    "https://ust-kamenogorsk.hh.kz/search/vacancy?area=194",
    headers={"User-Agent": "Mozilla/5.0"}
).text

idx = html.find("134222077")

fragment = html[max(0, idx-1000):idx+2000]

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": fragment[:4000]
    }
)

import requests
import os
import re

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = "https://ust-kamenogorsk.hh.kz/search/vacancy?area=194"

html = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
).text

matches = re.findall(r'/vacancy/(\d+)', html)

msg = (
    f"found={len(matches)}\n\n"
    + "\n".join(matches[:30])
)

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": msg[:4000]
    }
)

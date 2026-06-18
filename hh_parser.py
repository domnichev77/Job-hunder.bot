import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

all_vacancies = []

page = 0

while True:
    response = requests.get(
        "https://api.hh.ru/vacancies",
        params={
            "area": 160,      # Казахстан
            "page": page,
            "per_page": 100
        }
    )

    data = response.json()

    all_vacancies.extend(data["items"])

    if page >= data["pages"] - 1:
        break

    page += 1

message = (
    f"✅ Получено вакансий: {len(all_vacancies)}\n"
    f"Страниц обработано: {page + 1}"
)

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

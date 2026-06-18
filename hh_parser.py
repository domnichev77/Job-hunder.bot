import os
import requests
from bs4 import BeautifulSoup


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


URL = "https://ust-kamenogorsk.hh.kz/search/vacancy?area=194"


def get_vacancies():
    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    vacancies = []

    for item in soup.select('a[data-qa="serp-item__title"]'):
        title = item.get_text(
            " ",
            strip=True
        )

        link = item.get("href")

        if title and link:
            vacancies.append(
                {
                    "title": title,
                    "link": link
                }
            )

    return vacancies


def remove_duplicates(vacancies):
    result = []
    seen = set()

    for vacancy in vacancies:
        if vacancy["link"] not in seen:
            seen.add(vacancy["link"])
            result.append(vacancy)

    return result


def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message[:4000]
        },
        timeout=30
    )


def main():
    vacancies = get_vacancies()

    vacancies = remove_duplicates(
        vacancies
    )

    message = (
        f"Найдено вакансий: {len(vacancies)}\n\n"
    )

    for vacancy in vacancies[:10]:
        message += (
            f"{vacancy['title']}\n"
            f"{vacancy['link']}\n\n"
        )

    send_telegram(message)


if __name__ == "__main__":
    main()

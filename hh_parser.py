import os
import requests
from bs4 import BeautifulSoup


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


SEARCH_URL = "https://ust-kamenogorsk.hh.kz/search/vacancy?area=194"


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean(text):
    if not text:
        return ""

    return (
        text
        .replace("\n", " ")
        .replace("  ", " ")
        .strip()
    )


def get_links():

    html = requests.get(
        SEARCH_URL,
        headers=HEADERS,
        timeout=30
    ).text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    links = []

    for item in soup.select(
        'a[data-qa="serp-item__title"]'
    ):

        link = item.get("href")

        if link:
            links.append(
                link.split("?")[0]
            )

    return list(dict.fromkeys(links))



def get_vacancy(url):

    html = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    ).text


    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    def find(selector):

        item = soup.select_one(selector)

        if item:
            return clean(
                item.get_text(" ", strip=True)
            )

        return "Не указано"


    title = find(
        '[data-qa="vacancy-title"]'
    )

    company = find(
        '[data-qa="vacancy-company-name"]'
    )

    salary = find(
        '[data-qa="vacancy-salary"]'
    )

    description = find(
        '[data-qa="vacancy-description"]'
    )


    return {
        "title": title,
        "company": company,
        "salary": salary,
        "description": description,
        "url": url
    }



def format_description(text):

    if text == "Не указано":
        return text


    # режем слишком длинные описания
    if len(text) > 900:
        text = text[:900] + "..."


    replacements = [
        ("Обязанности:", "\n\n📋 Обязанности:\n"),
        ("Требования:", "\n\n👤 Требования:\n"),
        ("Мы предлагаем:", "\n\n🎁 Мы предлагаем:\n"),
        ("Условия:", "\n\n🕒 Условия:\n")
    ]


    for old, new in replacements:
        text = text.replace(
            old,
            new
        )


    return text



def send(message):

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message[:4000]
        },
        timeout=30
    )



def main():

    links = get_links()


    # пока тестируем 3 вакансии
    for link in links[:3]:

        vacancy = get_vacancy(link)


        description = format_description(
            vacancy["description"]
        )


        message = f"""
📌 {vacancy['title']}


🏢 Компания:
{vacancy['company']}


💰 Зарплата:
{vacancy['salary']}


📝 Описание:
{description}


🔗 Открыть вакансию:
{vacancy['url']}
"""


        send(message)



if __name__ == "__main__":
    main()

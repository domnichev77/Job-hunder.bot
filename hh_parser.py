import os
import requests
from bs4 import BeautifulSoup


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


SEARCH_URL = "https://ust-kamenogorsk.hh.kz/search/vacancy?area=194"


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_vacancy_links():

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

    for item in soup.select('a[data-qa="serp-item__title"]'):

        link = item.get("href")

        if link:
            links.append(link.split("?")[0])

    return list(dict.fromkeys(links))


def parse_vacancy(url):

    html = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    ).text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    title = soup.select_one(
        '[data-qa="vacancy-title"]'
    )

    salary = soup.select_one(
        '[data-qa="vacancy-salary"]'
    )

    company = soup.select_one(
        '[data-qa="vacancy-company-name"]'
    )

    description = soup.select_one(
        '[data-qa="vacancy-description"]'
    )


    return {

        "title":
            title.get_text(" ", strip=True)
            if title else "Нет данных",

        "salary":
            salary.get_text(" ", strip=True)
            if salary else "Доход не указан",

        "company":
            company.get_text(" ", strip=True)
            if company else "Компания не указана",

        "description":
            description.get_text(" ", strip=True)[:700]
            if description else "Описание отсутствует",

        "url":
            url
    }



def send_telegram(text):

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text[:4000]
        }
    )



def main():

    links = get_vacancy_links()


    message = (
        f"Найдено вакансий: {len(links)}\n\n"
    )


    for link in links[:5]:

        vacancy = parse_vacancy(link)


        message += (
            f"📌 {vacancy['title']}\n"
            f"🏢 {vacancy['company']}\n"
            f"💰 {vacancy['salary']}\n\n"
            f"{vacancy['description']}\n\n"
            f"🔗 {vacancy['url']}\n"
            f"----------------\n\n"
        )


    send_telegram(message)



if __name__ == "__main__":
    main()

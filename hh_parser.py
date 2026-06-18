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

    soup = BeautifulSoup(html, "html.parser")

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



def clean_text(text):

    if not text:
        return "Нет данных"

    return (
        text
        .replace("\n\n\n", "\n")
        .replace("  ", " ")
        .strip()
    )



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


    def get(selector):

        item = soup.select_one(selector)

        return clean_text(
            item.get_text(" ", strip=True)
        ) if item else "Не указано"



    return {

        "title": get(
            '[data-qa="vacancy-title"]'
        ),

        "company": get(
            '[data-qa="vacancy-company-name"]'
        ),

        "salary": get(
            '[data-qa="vacancy-salary"]'
        ),

        "description": get(
            '[data-qa="vacancy-description"]'
        ),

        "url": url
    }



def send(text):

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )



def main():

    links = get_vacancy_links()


    for link in links[:5]:


        vacancy = parse_vacancy(link)


        message = f"""
📌 {vacancy['title']}


🏢 Компания:
{vacancy['company']}


💰 Зарплата:
{vacancy['salary']}


📝 Описание:
{vacancy['description']}


🔗 Открыть вакансию:
{vacancy['url']}
"""


        send(message[:4000])



if __name__ == "__main__":
    main()

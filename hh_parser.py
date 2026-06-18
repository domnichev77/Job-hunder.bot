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



def parse(url):

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

        return clean(
            item.get_text(" ", strip=True)
        ) if item else ""


    title = get(
        '[data-qa="vacancy-title"]'
    )

    salary = get(
        '[data-qa="vacancy-salary"]'
    )

    description = get(
        '[data-qa="vacancy-description"]'
    )


    return {
        "title": title,
        "salary": salary,
        "description": description,
        "url": url
    }



def analyze(vacancy):

    score = 5

    plus = []
    minus = []


    text = (
        vacancy["description"]
        .lower()
    )


    if "без опыта" in text:
        score += 2
        plus.append(
            "можно без опыта"
        )


    if "200" in vacancy["salary"]:
        score += 1
        plus.append(
            "зарплата от 200к"
        )


    if "полный день" in text:
        plus.append(
            "полный день"
        )


    if "опыт" in text:
        minus.append(
            "есть требование по опыту"
        )


    return score, plus, minus



def send(text):

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )



def main():

    links = get_links()


    for link in links[:3]:

        vacancy = parse(link)

        score, plus, minus = analyze(vacancy)


        short = vacancy["description"][:400]


        message = f"""
📌 {vacancy['title']}


💰 {vacancy['salary']}


⭐ Оценка:
{score}/10


🟢 Плюсы:
{chr(10).join("• "+x for x in plus) if plus else "• нет данных"}


⚠️ Обратить внимание:
{chr(10).join("• "+x for x in minus) if minus else "• нет данных"}


📋 Коротко:
{short}


🔗 Открыть:
{vacancy['url']}
"""


        send(message)



if __name__ == "__main__":
    main()

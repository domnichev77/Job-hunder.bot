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

        if item:
            return clean(
                item.get_text(" ", strip=True)
            )

        return ""


    return {
        "title": get('[data-qa="vacancy-title"]'),
        "salary": get('[data-qa="vacancy-salary"]'),
        "description": get('[data-qa="vacancy-description"]'),
        "url": url
    }



def analyze(vacancy):

    text = (
        vacancy["description"]
        .lower()
    )

    score = 5

    plus = []
    minus = []


    good_words = [
        ("без опыта", "можно без опыта"),
        ("обучение", "есть обучение"),
        ("рассмотрим начинающих", "готовы рассмотреть новичков"),
        ("студент", "подходит студентам")
    ]


    bad_words = [
        ("от 3 лет", "требуется опыт от 3 лет"),
        ("обязателен опыт", "опыт обязателен"),
        ("руководящ", "руководящий опыт")
    ]


    for word, reason in good_words:

        if word in text:
            score += 1
            plus.append(reason)


    for word, reason in bad_words:

        if word in text:
            score -= 1
            minus.append(reason)


    if "200" in vacancy["salary"]:
        score += 1
        plus.append("зарплата от 200 000 ₸")


    if not plus:
        plus.append(
            "особых преимуществ не найдено"
        )


    if not minus:
        minus.append(
            "критичных минусов не найдено"
        )


    if score < 1:
        score = 1

    if score > 10:
        score = 10


    return score, plus, minus



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

    links = get_links()


    for link in links[:3]:

        vacancy = parse(link)

        score, plus, minus = analyze(
            vacancy
        )


        description = vacancy["description"]


        if len(description) > 400:
            description = (
                description[:400]
                + "..."
            )


        message = f"""
📌 {vacancy['title']}


💰 Доход:
{vacancy['salary']}


⭐ Оценка:
{score}/10


Почему:


➕ Плюсы:
{chr(10).join("• " + x for x in plus)}


⚠️ Обратить внимание:
{chr(10).join("• " + x for x in minus)}


📝 Коротко:
{description}


🔗 Открыть:
{vacancy['url']}
"""


        send(message)



if __name__ == "__main__":
    main()

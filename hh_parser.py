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


        return "Не указано"



    return {

        "title": get(
            '[data-qa="vacancy-title"]'
        ),

        "salary": get(
            '[data-qa="vacancy-salary"]'
        ),

        "description": get(
            '[data-qa="vacancy-description"]'
        ),

        "url": url

    }



def analyze(vacancy):

    text = (
        vacancy["description"]
        .lower()
    )


    score = 5

    reasons = []


    if (
        "без опыта" in text
        or "обучение" in text
        or "рассмотрим" in text
    ):

        score += 2

        reasons.append(
            "Есть признаки, что готовы рассматривать новичков"
        )

    else:

        reasons.append(
            "Нет явного указания на работу без опыта"
        )



    if (
        "1–3 года" in text
        or "1-3 года" in text
    ):

        score += 1

        reasons.append(
            "Опыт 1–3 года подходит как начальный уровень"
        )



    if "от 3 лет" in text:

        score -= 2

        reasons.append(
            "Требуется опыт от 3 лет"
        )



    if "200" in vacancy["salary"]:

        score += 1

        reasons.append(
            "Доход начинается от 200 000 ₸"
        )



    if "150" in vacancy["salary"]:

        reasons.append(
            "Нижняя граница дохода ниже желаемого уровня"
        )



    if score >= 8:

        conclusion = (
            "Сильное совпадение — стоит смотреть"
        )

    elif score >= 5:

        conclusion = (
            "Средний вариант — зависит от твоего опыта"
        )

    else:

        conclusion = (
            "Слабое совпадение"
        )



    if score < 1:
        score = 1


    if score > 10:
        score = 10



    return score, reasons, conclusion



def send(message):

    requests.post(

        f"https://api.telegram.org/bot{TOKEN}/sendMessage",

        data={

            "chat_id": CHAT_ID,

            "text": message,

            "parse_mode": "HTML"

        },

        timeout=30

    )



def main():

    links = get_links()



    for link in links[:3]:

        vacancy = parse(link)


        score, reasons, conclusion = analyze(
            vacancy
        )


        description = vacancy["description"]


        if len(description) > 450:

            description = (
                description[:450]
                + "..."
            )



        message = f"""

<b>📌 {vacancy['title']}</b>


<b>💰 Доход</b>
{vacancy['salary']}


<b>🎯 Совпадение: {score}/10</b>


<b>Почему такая оценка:</b>
{chr(10).join("• " + x for x in reasons)}


<b>💡 Вывод:</b>
{conclusion}


<b>📝 Коротко:</b>
{description}


<b>🔗 Открыть вакансию:</b>
{vacancy['url']}

"""


        send(message)



if __name__ == "__main__":

    main()

import os
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = "https://ust-kamenogorsk.hh.kz/search/vacancy?area=194"

response = requests.get(
url,
headers={"User-Agent": "Mozilla/5.0"},
timeout=30
)

soup = BeautifulSoup(response.text, "html.parser")

vacancies = []

for a in soup.select('a[data-qa="serp-item__title"]'):
title = a.get_text(strip=True)
link = a.get("href")

```
if title and link:
    vacancies.append((title, link))
```

# убираем дубли

seen = set()
unique = []

for title, link in vacancies:
if link not in seen:
seen.add(link)
unique.append((title, link))

message = f"Найдено вакансий: {len(unique)}\n\n"

for title, link in unique[:10]:
message += f"{title}\n{link}\n\n"

requests.post(
f"https://api.telegram.org/bot{TOKEN}/sendMessage",
data={
"chat_id": CHAT_ID,
"text": message[:4000]
}
)

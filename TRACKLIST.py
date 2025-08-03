import requests
import random
from bs4 import BeautifulSoup

# ЗАГОТОВКА ЧЕРЕЗ РЕКВЕСТ

base_url = "https://www.1001tracklists.com"
search_url = "https://www.1001tracklists.com/search/result.php"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/91.0",
]

referers = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://duckduckgo.com/",
]

accept_languages = [
    "en-US,en;q=0.9",
    "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Referer": random.choice(referers),
    "Accept-Language": random.choice(accept_languages),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
}

track = "Adam Ten & Rhye - 3 Days Later"

payload = {
    "main_search": track,
    "search_selection": "2",  # 2 = поиск tracks
    "orderby": "added",
}

response = requests.post(search_url, data=payload, headers=headers)
print(response.status_code)

found_link = None
found_photo_url = None
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    blocks = soup.select("div.bItm.oItm")
    for block in blocks:
        link = block.select_one("div > a")
        if link and link.text.strip() == track:
            img = block.find("img", class_="artM")
            found_photo_url = img.get("data-src") or img.get("src") if img else None
            found_link = link["href"]
            break
else:
    print("Ошибка загрузки:", response.status_code)

print(f"found_link: {found_link}")
print(f"found_photo_url: {found_photo_url}")

next_url = base_url + found_link
response = requests.get(next_url, headers=headers)
print(response.url)  # убедись, что попал на нужную страницу
next_next_url = None
mix_name = None

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    blocks = soup.select("div.bItm.action.oItm")
    print(f"Найдено блоков: {len(blocks)}")

    for block in blocks:
        link = block.select_one("a")
        if link and link.has_attr("href"):
            next_next_url = link["href"]
            mix_name = link.text.strip()
            break

else:
    print("Ошибка загрузки:", response.status_code)

print(f"next_next_url: {next_next_url}")
print(f"mix_name: {mix_name}")

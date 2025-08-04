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

def get_random_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Referer": random.choice(referers),
        "Accept-Language": random.choice(accept_languages),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }



payload = {
    "main_search": track,
    "search_selection": "2",  # 2 = поиск tracks
    "orderby": "added",
}

track = "Adam Ten & Rhye - 3 Days Later"

response = requests.post(search_url, data=payload, headers=get_random_headers())
response.raise_for_status()
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
response = requests.get(next_url, headers=get_random_headers())
response.raise_for_status()
print(response.url)
next_found_link = None
mix_name = None

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    blocks = soup.select("div.bItm.action.oItm")
    print(f"Найдено блоков: {len(blocks)}")

    for block in blocks:
        link = block.select_one("a")
        if link and link.has_attr("href"):
            next_found_link = link["href"]
            mix_name = link.text.strip()
            break

else:
    print("Ошибка загрузки:", response.status_code)

print(f"next_next_url: {next_found_link}")
print(f"mix_name: {mix_name}")


next_next_url = base_url + next_found_link
print(f"next_next_url: {next_next_url}")
target_track_id = None
target_track_name = None
tracks = {}

try:
    response = requests.get(next_next_url, headers=get_random_headers(), timeout=10)
    response.raise_for_status()
    print(response.url)
except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e}")

else:
    soup = BeautifulSoup(response.text, "html.parser")
    blocks = soup.select("#tlTab > div")
    print(f"Найдено блоков: {len(blocks)}")
    for block in blocks:
        meta_tag = block.select_one("meta")
        target_track_name = meta_tag.get("content") if meta_tag else None

        if target_track_name and track in target_track_name:
            target_track_id = int(block.get('data-trno'))
            print(f'Найден искомый трек: ID({target_track_id}) name:{target_track_name}')
            break
    if target_track_id:
        tracks[target_track_id] = target_track_name
        for block in blocks:
            try:
                track_id = int(block.get('data-trno'))
            except (TypeError, ValueError):
                continue

            if track_id == target_track_id - 1:
                meta_tag = block.select_one("meta")
                target_track_name = meta_tag.get("content") if meta_tag else None
                tracks[track_id] = target_track_name

            if track_id == target_track_id + 1:
                meta_tag = block.select_one("meta")
                target_track_name = meta_tag.get("content") if meta_tag else None
                tracks[track_id] = target_track_name

    if (target_track_id - 1) not in tracks and (target_track_id + 1) not in tracks:
        print("Соседние треки не найдены")

    print(tracks)


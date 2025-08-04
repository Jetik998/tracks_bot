import requests
import random
from bs4 import BeautifulSoup
import time

# ЗАГОТОВКА ЧЕРЕЗ РЕКВЕСТ

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
    """
    Функция для рандомных заголовков
    :return:
    """
    return {
        "User-Agent": random.choice(user_agents),
        "Referer": random.choice(referers),
        "Accept-Language": random.choice(accept_languages),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }

def random_sleep(min_sec=2, max_sec=6):
    """
    Пауза на случайное время между min_sec и max_sec секундами с выводом в консоль.
    """
    sleep_time = random.uniform(min_sec, max_sec)
    print(f"[*] Ждём {sleep_time:.1f} сек перед следующим запросом")
    time.sleep(sleep_time)

def words_similarity(input_track, found_track, threshold=0.6):
    """
    Сравнивает названия треков по совпадению слов.

    Возвращает True, если (по умолчанию) 60% слов из input_track
    содержатся в found_track, иначе False.
    """
    input_words = input_track.lower().split()
    found_words = found_track.lower().split()

    matches = sum(1 for w in input_words if w in found_words)
    similarity = matches / len(input_words)

    return similarity >= threshold

def make_request(session, url, payload, retries=3):
    """Отправляет POST-запрос с повторами при ошибках"""
    for attempt in range(retries):
        try:
            timeout = (random.uniform(3, 6), random.uniform(10, 20))
            response = requests.post(url, headers=get_random_headers(), data=payload, timeout=timeout)
            response.raise_for_status()  # выбросит ошибку если код != 200
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"[!] Ошибка: {e}. Попытка {attempt+1}/{retries}...")
            time.sleep(random.uniform(2, 5))  # пауза перед повтором
    raise RuntimeError("Все попытки выполнить запрос не удались. Прерывание программы.")

track_search_limit = 10
track = {}
track_name = "Adam Ten & Rhye - 3 Days Later"
track["name"] = track_name
track_id = None
found_link = None


payload = {
    "main_search": track_name,
    "search_selection": "2",  # пункт 2 = поиск tracks на сайте
    "orderby": "added",
}

base_url = "https://www.1001tracklists.com"
search_url = "https://www.1001tracklists.com/search/result.php"
max_checks = 10
checks_done = 0

with requests.Session() as session:

    #Step 1 (Получение первой ссылки из поиска)
    html = make_request(session, search_url, payload)
    soup = BeautifulSoup(html, "html.parser")
    blocks = soup.select("#kTZXcvbn > div.bItm.oItm")

    for block in blocks:
        if checks_done >= max_checks:
            print("Достигнут лимит проверок, трек не найден.")
            break

        found_tag = block.select_one("div.bCont.acSA > div.bTitle > a")
        if not found_tag:
            checks_done += 1
            continue

        # Берём название трека из текста тега <a>
        found_track_name = found_tag.text
        # Сравниваем название найденного трека с нашим входным
        if words_similarity(track_name, found_track_name, threshold=0.6):
            img_tag = block.select_one("img")
            if img_tag:
                track_img = img_tag.get("data-src")
            found_link = found_tag.get("href")
            if found_link:
                track["link"] = found_link
                break

    if found_link:
        checks_done = 0
        # Step 2
        html = make_request(session, search_url, payload)
        soup = BeautifulSoup(html, "html.parser")
        blocks = soup.select("#kTZXcvbn > div.bItm.action.oItm")

        for block in blocks:
            if checks_done >= max_checks:
                print("Достигнут лимит проверок, трек не найден.")
                break

            found_tag = block.select_one("div.bCont > div.bTitle > a")
            if not found_tag:
                checks_done += 1
                continue

            # Берём название трека из текста тега <a>
            found_track_name = found_tag.text
            # Сравниваем название найденного трека с нашим входным
            if words_similarity(track_name, found_track_name, threshold=0.6):
                img_tag = block.select_one("img")
                if img_tag:
                    track_img = img_tag.get("data-src")
                found_link = found_tag.get("href")
                if found_link:
                    track["link"] = found_link
                    break

    else:
        print(f"Ссылка не найдена {found_link}")
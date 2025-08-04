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
    sleep_time = random.uniform(min_sec, max_sec)
    print(f"[*] Ждём {sleep_time:.1f} сек перед следующим запросом")
    time.sleep(sleep_time)

def word_match_ratio(track_name, found_text):
    """Возвращает процент совпадения по словам."""
    t_words = set(track_name.lower().split())
    f_words = set(found_text.lower().split())

    # количество общих слов
    common = t_words & f_words
    ratio = len(common) / len(t_words) * 100  # процент совпадения

    return ratio

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

track = "Adam Ten & Rhye - 3 Days Later"
track_id = None
track_img = None

payload = {
    "main_search": track,
    "search_selection": "2",  # 2 = поиск tracks
    "orderby": "added",
}

base_url = "https://www.1001tracklists.com"
search_url = "https://www.1001tracklists.com/search/result.php"


with requests.Session() as session:

    html = make_request(session, search_url, payload)
    soup = BeautifulSoup(html, "html.parser")
    blocks = soup.select("#kTZXcvbn > div.bItm.oItm")
    for block in blocks:
        link = block.select_one("div.bCont.acSA > div.bTitle > a")
        if link


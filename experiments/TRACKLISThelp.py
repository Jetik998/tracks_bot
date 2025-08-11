
track = "Adam Ten & Rhye - 3 Days Later"

# Step 1
response = requests.post(search_url, data=payload, headers=get_random_headers())
response.raise_for_status()
print(response.status_code)

import requests
import random
import time

# --- ДАННЫЕ ДЛЯ ЗАГОЛОВКОВ ---
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

# --- ФУНКЦИЯ ДЛЯ РАНДОМНЫХ ЗАГОЛОВКОВ ---
def get_random_headers():
    return {
        "User-Agent": random.choice(user_agents),
        "Referer": random.choice(referers),
        "Accept-Language": random.choice(accept_languages),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }

# --- ФУНКЦИЯ С ЗАПРОСОМ ---
def make_request(url, payload, retries=3):
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
    return None  # если все попытки неудачные

# --- ПРИМЕР ИСПОЛЬЗОВАНИЯ ---
url = "https://example.com/search"
payload = {
    "main_search": "track_name",
    "search_selection": "2",
    "orderby": "added",
}

for i in range(5):
    html = make_request(url, payload)
    if html:
        print(f"[+] Запрос {i+1} выполнен успешно ({len(html)} символов)")
    else:
        print(f"[-] Запрос {i+1} не удался")

    # --- Рандомная пауза между запросами ---
    sleep_time = random.uniform(2, 6)
    print(f"[*] Ждём {sleep_time:.1f} сек перед следующим запросом")
    time.sleep(sleep_time)


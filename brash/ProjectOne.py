import cloudscraper
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

def words_sim(input_track, found_track, threshold=0.6):
    """
    Сравнивает названия треков по совпадению слов.

    Возвращает True, если (по умолчанию) 60% слов из input_track
    содержатся в found_track, иначе False.
    """
    input_words = input_track.lower().split()
    found_words = found_track.lower().split()

    matches = sum(1 for w in input_words if w in found_words)
    similarity = matches / len(input_words)

    print(f'Сравнение треков: {similarity >= threshold}')
    return similarity >= threshold

scraper = cloudscraper.create_scraper()

def make_request(url, payload, retries=3):
    #Отправляет POST-запрос с повторами при ошибках через cloudscraper
    for attempt in range(retries):
        try:
            response = scraper.post(url, headers=get_random_headers(), data=payload)
            response.raise_for_status()
            with open("../response.html", "w", encoding="utf-8") as f:
                f.write(response.text)
            return response.text
        except Exception as e:
            print(f"[!] Ошибка: {e}. Попытка {attempt+1}/{retries}...")
            time.sleep(random.uniform(2, 5))  # пауза перед повтором
    raise RuntimeError("Все попытки выполнить запрос не удались. Прерывание программы.")

track_search_limit = 10
track_name = "Adam Ten & Rhye - 3 Days Later"
track_link = None
track_id = None
found_link = None
mix_search_limit = 10
to_mix_search_limit = 30


payload = {
    "main_search": track_name,
    "search_selection": "2",  # пункт 2 = поиск tracks на сайте
    "orderby": "added",
}

base_url = "https://www.1001tracklists.com"
search_url = "https://www.1001tracklists.com/search/result.php"

max_checks = 10
checks_done = 0


#Step 1 (Найти страницу трека в поиске)
html = make_request(search_url, payload)
soup = BeautifulSoup(html, "html.parser")
blocks = soup.select("div.bItm.oItm")

print('Первый цикл')
for block in blocks:
    print('Вошли в цикл')
    if checks_done >= max_checks:
        print("Достигнут лимит проверок, трек не найден. step 1")
        break

    found_tag = block.select_one("div.bCont.acSa > div.bTitle > a")
    print(f'Первый тег{found_tag.text}')
    if not found_tag:
        checks_done += 1
        continue

    print('Нейм найден')
    # Берём название трека из текста тега <a>
    found_track_name = found_tag.text
    print('{found_track_name}')
    # Сравниваем название найденного трека с нашим входным
    if words_sim(track_name, found_track_name, threshold=0.6):
        #Обновляем трек нейм на найденный из тега
        track_name = found_track_name
        img_tag = block.select_one("img")
        if img_tag:
            track_img = img_tag.get("data-src")
        found_link = found_tag.get("href")
        if found_link:
            track_link = found_link
            break

if track_link:
    # Объединяем базовый URL с найденным
    track_link = base_url + track_link
    # Обнуляем счетчик
    checks_done = 0
    # Step 2 (Ищем ссылки на миксы > Переходим в миксы
    # > Ищем название трека в миксах)
    found_mix_name = None
    found_mix_link = None
    html = make_request(track_link, payload)
    soup = BeautifulSoup(html, "html.parser")
    blocks = soup.select("#kTZXcvbn > div.bItm.action.oItm")

    for block in blocks:
        if checks_done >= mix_search_limit:
            print("Достигнут лимит проверок, микс не найден. step 2")
            break

        found_tag = block.select_one("div.bCont > div.bTitle > a")
        if not found_tag:
            checks_done += 1
            continue

        # Берём название микса из текста тега <a>
        found_mix_name = found_tag.text
        found_mix_link = found_tag.get("href")

        # Если ссылка найдена, переходим в микс и ищем наш трек.
        if found_mix_link:
            # Обнуляем счетчик
            checks_done = 0

            found_mix_link = base_url + found_mix_link
            mix_html = make_request(found_mix_link, payload)
            soup = BeautifulSoup(mix_html, "html.parser")
            items = soup.select("#tlTab > div")

            #Цикл поиска id Базового трека
            for item in items:
                if checks_done >= to_mix_search_limit:
                    print("Достигнут лимит проверок, трек в миксе не найден. step 3")
                    break

                found_tag_base = item.select_one("div.bCont.tl")
                if not found_tag_base:
                    checks_done += 1
                    continue

                #Если нашли id Базового трека
                meta_tag = item.select_one("meta")
                target_track_name = meta_tag.get("content") if meta_tag else None

                if target_track_name == track_name:
                    track_id = block.get('data-trno')
                    break

            #Нашли id нашего трека > Ищем соседние id
            if track_id:
                # Обнуляем счетчик
                checks_done = 0
                base_id = int(track_id)
                prev_id = str(base_id - 1)
                next_id = str(base_id + 1)
                prev_track_name = None
                next_track_name = None
                for item in items:
                    if checks_done >= to_mix_search_limit:
                        print("Достигнут лимит проверок, трек в миксе не найден. step 4")
                        break

                    get_id = block.get('data-trno')
                    if not get_id:
                        checks_done += 1
                        continue

                    if get_id == prev_id:
                        meta_tag = item.select_one("meta")
                        target_track_name = meta_tag.get("content") if meta_tag else None
                        prev_track_name = target_track_name

                    if get_id == next_id:
                        meta_tag = item.select_one("meta")
                        target_track_name = meta_tag.get("content") if meta_tag else None
                        next_track_name = target_track_name

                if not prev_track_name and not next_track_name:
                    print("Ни одного трека не найдено")

                else:
                    print(f"Предыдущий трек: {prev_track_name}\nСледующий трек: {next_track_name}")












else:
    print(f"Ссылка не найдена {found_link}")
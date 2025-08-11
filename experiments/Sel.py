import random
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


def random_sleep(min_sec=2, max_sec=6):
    sleep_time = random.uniform(min_sec, max_sec)
    print(f"[*] Ждём {sleep_time:.1f} сек перед следующим запросом")
    time.sleep(sleep_time)

def words_sim(input_track, found_track, threshold=0.6):
    input_words = input_track.lower().split()
    found_words = found_track.lower().split()
    matches = sum(1 for w in input_words if w in found_words)
    similarity = matches / len(input_words)
    print(f'Сравнение треков: {similarity} (>= {threshold}) -> {similarity >= threshold}')
    return similarity >= threshold


def make_request_search(url, search_text, search_selection="2"):
    """
    Выполняет поиск на сайте и возвращает HTML страницы с результатами.
    Отдельная функция для поиска — форма отправляется один раз.
    """
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(url)

        search_input = wait.until(EC.presence_of_element_located((By.NAME, "main_search")))
        search_input.clear()
        search_input.send_keys(search_text)

        driver.execute_script(
            'document.getElementsByName("search_selection")[0].value = arguments[0];',
            search_selection
        )

        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type=submit]")))
        submit.click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.bItm.oItm")))
        html = driver.page_source
        return html

    except Exception as e:
        print(f"[!] Ошибка в make_request_search: {e}")
        return ""
    finally:
        driver.quit()


def make_request_page(url):
    """
    Загружает страницу без поиска, просто получает HTML.
    """
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        html = driver.page_source
        return html

    except Exception as e:
        print(f"[!] Ошибка в make_request_page: {e}")
        return ""
    finally:
        driver.quit()


def main():
    track_name = "Adam Ten & Rhye - 3 Days Later"
    base_url = "https://www.1001tracklists.com"
    search_url = base_url + "/search/result.php"

    # Шаг 1: Поиск трека
    html = make_request_search(search_url, track_name, search_selection="2")
    if not html:
        print("[!] Не удалось получить страницу поиска")
        return

    soup = BeautifulSoup(html, "html.parser")
    blocks = soup.select("div.bItm.oItm")

    max_checks = 10
    checks_done = 0
    track_link = None
    found_track_name = None

    for block in blocks:
        if checks_done >= max_checks:
            print("Достигнут лимит проверок, трек не найден. step 1")
            break

        found_tag = block.select_one("div.bCont.acSa > div.bTitle > a")
        if not found_tag:
            checks_done += 1
            continue

        candidate_name = found_tag.text.strip()
        print(f"Найден трек: {candidate_name}")

        if words_sim(track_name, candidate_name, threshold=0.6):
            track_link = found_tag.get("href")
            found_track_name = candidate_name
            break

        checks_done += 1

    if not track_link:
        print("Ссылка на трек не найдена.")
        return

    track_link = base_url + track_link
    print(f"Ссылка на страницу трека: {track_link}")
    track_name = found_track_name  # обновляем название трека

    # Шаг 2: Поиск миксов трека
    html = make_request_page(track_link)
    if not html:
        print("[!] Не удалось получить страницу трека")
        return

    soup = BeautifulSoup(html, "html.parser")
    blocks = soup.select("#kTZXcvbn > div.bItm.action.oItm")

    mix_search_limit = 10
    checks_done = 0
    track_id = None

    for block in blocks:
        if checks_done >= mix_search_limit:
            print("Достигнут лимит проверок, микс не найден. step 2")
            break

        found_tag = block.select_one("div.bCont > div.bTitle > a")
        if not found_tag:
            checks_done += 1
            continue

        found_mix_name = found_tag.text.strip()
        found_mix_link = found_tag.get("href")

        if not found_mix_link:
            checks_done += 1
            continue

        found_mix_link = base_url + found_mix_link
        print(f"Проверяем микс: {found_mix_name} ({found_mix_link})")

        # Шаг 3: Ищем трек в миксе
        mix_html = make_request_page(found_mix_link)
        if not mix_html:
            print(f"[!] Не удалось получить страницу микса {found_mix_name}")
            checks_done += 1
            continue

        soup_mix = BeautifulSoup(mix_html, "html.parser")
        items = soup_mix.select("#tlTab > div")

        to_mix_search_limit = 30
        found = False
        for item in items:
            if checks_done >= to_mix_search_limit:
                print("Достигнут лимит проверок, трек в миксе не найден. step 3")
                break

            found_tag_base = item.select_one("div.bCont.tl")
            if not found_tag_base:
                checks_done += 1
                continue

            meta_tag = item.select_one("meta")
            target_track_name = meta_tag.get("content").strip() if meta_tag else None

            if target_track_name == track_name:
                track_id = item.get('data-trno')
                found = True
                print(f"Найден трек в миксе с id: {track_id}")
                break

            checks_done += 1

        if found:
            # Шаг 4: Ищем соседние треки по id
            base_id = int(track_id)
            prev_id = str(base_id - 1)
            next_id = str(base_id + 1)

            prev_track_name = None
            next_track_name = None

            for item in items:
                get_id = item.get('data-trno')
                if not get_id:
                    continue

                meta_tag = item.select_one("meta")
                target_name = meta_tag.get("content").strip() if meta_tag else None

                if get_id == prev_id:
                    prev_track_name = target_name
                elif get_id == next_id:
                    next_track_name = target_name

            print(f"Предыдущий трек: {prev_track_name}")
            print(f"Следующий трек: {next_track_name}")
            break

        checks_done += 1

    if not track_id:
        print("Трек в миксах не найден.")


if __name__ == "__main__":
    main()

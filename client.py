import logging
import random
import time
import cloudscraper
from utils import load_cookies, save_cookies

logger = logging.getLogger(__name__)

scraper = cloudscraper.create_scraper()

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
    """
    return {
        "User-Agent": random.choice(user_agents),
        "Referer": random.choice(referers),
        "Accept-Language": random.choice(accept_languages),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }


load_cookies(scraper)


def get_html(url, data=None):
    """Выполняет POST-запрос с рандомными заголовками"""
    global scraper
    get_html.count += 1
    time.sleep(random.uniform(1, 5))
    headers = get_random_headers()
    try:
        response = scraper.post(url, headers=headers, data=data)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Ошибка при запросе: {e}")
        raise
    save_cookies(scraper)
    get_html.last_url = response.url
    logger.info(f"Последняя ссылка: {get_html.last_url}")
    return response.text


get_html.last_url = ""
get_html.count = 0

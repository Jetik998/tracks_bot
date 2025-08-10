import logging
from bs4 import BeautifulSoup
from utils import save_to_file, save_captcha_image
from client import get_html
from config import *

logger = logging.getLogger(__name__)

input_track_url = None

def search_track():
    """Ищет трек по названию, возвращает страницу со списком треков"""
    payload = {
        "main_search": INPUT_TRACK,
        "search_selection": "2",  # 2 = поиск tracks
        "orderby": "added",
    }
    html = get_html(SEARCH_URL, data=payload)
    save_to_file(html, "InputTrackPage.html")
    return html

def detect_captcha(html):
    """Возвращает True, если капча есть, иначе False"""
    soup = BeautifulSoup(html, "html.parser")
    if soup.find('div', id='kTZXcvbn'):
        logger.info("Ввод капчи не потребовался")
        return False
    else:
        logger.info("Нужно ввести капчу")
        return True

def get_input_track_url(html):
    """Принимает страницу со списком треков, ищет совпадение с искомым треком
    Если трек найден, возвращает ссылку на страницу с треком"""
    global input_track_url
    soup = BeautifulSoup(html, "html.parser")
    tracks_dives = soup.select("div.bItm.oItm")
    count = 0
    for div in tracks_dives:
        count += 1
        logger.info(f'{count} Попытка поиска искомого трека')
        if count <=10:
            link = div.select_one("div.bCont.acSa > div.bTitle > a")
            if link and link.text.strip() == INPUT_TRACK:
                input_track_url = link.get("href")
                input_track_url = BASE_URL + input_track_url
                logger.info(f"Найдена ссылка на искомый трек {input_track_url}")
                return input_track_url

        else:
            logger.info(f'Сделано {count} попыток поиска треков.')

def solve_captcha(html):
    """Принимает страницу, находит капчу, сохряняет в jpg"""
    soup = BeautifulSoup(html, "html.parser")
    captcha_img = soup.find('img', alt='Captcha')
    if captcha_img:
        captcha_url = captcha_img.get('src')
        save_captcha_image(captcha_url)
        logger.error("Появилась страница с капчей, изображение сохранено.")
        #captcha_input = input("Введите капчу: ")

    else:
        logger.info("Капча не найдена")



def search_url_input_track():
    """Ищет страницу для (input_track). Возвращает ссылку если найдено совпадение."""
    html = search_track()
    if detect_captcha(html):
        solve_captcha(html)

    url = get_input_track_url(html)
    logger.info("search_url_input_track: Выполнено!")
    return url


def load_page_input_track(url):
    """Принимает ссылку на страницу (input_track),
     переходит на страницу с треком, проверяет есть ли капча,
     возвращает страницу.
    """
    html = get_html(url)
    if detect_captcha(html):
        solve_captcha(html)

    logger.info("load_page_input_track: Выполнено!")
    return html

def search_mixes_on_page(html):
    count = 0
    soup = BeautifulSoup(html, "html.parser")
    mix_dives = soup.select("#kTZXcvbn > div.bItm.action.oItm")
    for div in mix_dives:
        count += 1
        if count >= MIX_RETRY_COUNT:
            logger.info(f'Количество попыток поиска миксов: %s', count)
        if count >= MIX_COUNT_LIMIT:
            logger.info(f'Количество найденных миксов: %s', count)
            logger.info(f'{mix_count} Попытка поиска микса')
            mix_link = div.select_one("div.bCont > div.bTitle > a")
            mix_name = mix_link.text.strip()
            mix_url = mix_link.get('href')
            mix_url = BASE_URL + mix_url







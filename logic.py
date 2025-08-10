import logging
import base64
from bs4 import BeautifulSoup
from utils import save_to_file
from client import get_html



#time.sleep(random.uniform(1, 5))

logger = logging.getLogger(__name__)


input_track = "Adam Ten & Rhye - 3 Days Later"
input_track_url = None
base_url = "https://www.1001tracklists.com"


def search_track():
    """Ищет трек по названию, возвращает страницу со списком треков"""
    global input_track
    payload = {
        "main_search": input_track,
        "search_selection": "2",  # 2 = поиск tracks
        "orderby": "added",
    }
    search_url = "https://www.1001tracklists.com/search/result.php"
    html = get_html(search_url, data=payload)
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
    global base_url, input_track_url
    soup = BeautifulSoup(html, "html.parser")
    tracks_dives = soup.select("div.bItm.oItm")
    count = 0
    for div in tracks_dives:
        count += 1
        logger.info(f'{count} Попытка поиска искомого трека')
        if count <=10:
            url = div.select_one("div.bCont.acSa > div.bTitle > a")
            if url and url.text.strip() == input_track:
                input_track_url = url.get("href")
                input_track_url = base_url + input_track_url
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
    pass





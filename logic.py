import logging
import base64
from bs4 import BeautifulSoup
from click import argument

from client import get_html
import os
import time
from datetime import datetime

#time.sleep(random.uniform(1, 5))

logger = logging.getLogger(__name__)

def generate_filename(prefix, filetype=""):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # миллисекунды
    filename = f"{prefix}_{timestamp}"

    if not filetype:
        filetype = ""
    elif not filetype.startswith("."):
        filetype = "." + filetype

    return f"{filename}{filetype}"

def save_to_file(html, prefix, filetype=""):
    filename = generate_filename(prefix, filetype)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
        logger.info(f'Файл {filename} сохранен.')

def save_captcha_image(url):
    img_dir = "img"
    os.makedirs(img_dir, exist_ok=True)

    image_data = url.split(",")[1]
    image_data = base64.b64decode(image_data)

    image_name = f"captcha_{int(time.time() * 1000)}.jpg"
    file_path = os.path.join(img_dir, image_name)

    with open(file_path, "wb") as f:
        f.write(image_data)

    logger.info(f'Изображение капчи {image_name} сохранено')

input_track = "Adam Ten & Rhye - 3 Days Later"
input_track_url = None
base_url = "https://www.1001tracklists.com"


def search_track():
    """Получение html результатов поиска"""
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
    soup = BeautifulSoup(html, "html.parser")
    captcha_img = soup.find('img', alt='Captcha')
    if captcha_img:
        captcha_url = captcha_img.get('src')
        save_captcha_image(captcha_url)
        #captcha_input = input("Введите капчу: ")

    else:
        logger.info("Капча не найдена")

def step1():
    html = search_track()
    if detect_captcha(html):
        solve_captcha(html)
    else:
        url = get_input_track_url(html)


def step2(url):
    html = get_html(url)
    if detect_captcha(html):
        solve_captcha(html)
    else:

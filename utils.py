from datetime import datetime
import logging
import pickle
import time
import base64
import os

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

def load_cookies(scraper, filename="cookies/cookies.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            cookies = pickle.load(f)
            scraper.cookies.update(cookies)
        logger.info("Куки загружены из файла")
    else:
        logger.info("Файл с куки не найден")

def save_cookies(scraper, filename="cookies/cookies.pkl"):
    folder = os.path.dirname(filename)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
        logger.info(f'Создана папка: {folder}')
    with open(filename, "wb") as f:
        pickle.dump(scraper.cookies, f)
    logger.info("Куки сохранены в файл")

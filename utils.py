from datetime import datetime
import logging
import pickle
import time
import base64
import os
import json

logger = logging.getLogger(__name__)


def generate_filename(prefix, filetype=""):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # миллисекунды
    filename = f"{prefix}_{timestamp}"

    if not filetype:
        filetype = ""
    elif not filetype.startswith("."):
        filetype = "." + filetype

    return f"{filename}{filetype}"


def save_to_file(html, prefix, filetype="", folder_name="saved_files"):
    try:
        # Путь к папке рядом со скриптом + folder_name
        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(script_dir, folder_name)

        # Создаём папку, если её нет
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            logging.info(f"Создана папка: {save_dir}")

        # Формируем имя файла с префиксом и расширением
        filename = generate_filename(prefix, filetype)
        filepath = os.path.join(save_dir, filename)

        # Сохраняем файл
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        logging.info(f"Файл {filepath} сохранен.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении файла: {e}")


def save_captcha_image(url):
    try:
        img_dir = "img"
        os.makedirs(img_dir, exist_ok=True)

        image_data = url.split(",")[1]
        image_data = base64.b64decode(image_data)

        image_name = f"captcha_{int(time.time() * 1000)}.jpg"
        file_path = os.path.join(img_dir, image_name)

        with open(file_path, "wb") as f:
            f.write(image_data)

        logger.info(f"Изображение капчи {image_name} сохранено")
    except Exception as e:
        logger.error(f"Ошибка при сохранении капчи: {e}")


def load_cookies(scraper, filename="cookies/cookies.pkl"):
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f:
                cookies = pickle.load(f)
            scraper.cookies.update(cookies)
            logger.info("Куки загружены из файла")
        except Exception as e:
            logger.error(f"Ошибка при загрузке куки из файла: {e}")
    else:
        logger.info("Файл с куки не найден")


def save_cookies(scraper, filename="cookies/cookies.pkl"):
    try:
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
            logger.info(f"Создана папка: {folder}")
        with open(filename, "wb") as f:
            pickle.dump(scraper.cookies, f)
        logger.info("Куки сохранены в файл")
    except Exception as e:
        logger.error(f"Ошибка при сохранении куки: {e}")


def save_to_json(data, prefix, folder_name="json"):
    try:
        # Получаем путь к папке рядом со скриптом
        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(script_dir, folder_name)

        # Создаём папку, если нет
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        # Формируем имя файла и полный путь
        filename = generate_filename(prefix, "json")
        filepath = os.path.join(save_dir, filename)

        # Сохраняем файл
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Данные успешно сохранены в файл {filepath}")
    except (IOError, OSError) as e:
        logging.error(f"Ошибка при записи файла {filepath}: {e}")
    except TypeError as e:
        logging.error(f"Ошибка сериализации данных в JSON: {e}")

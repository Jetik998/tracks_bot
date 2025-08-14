from datetime import datetime
import logging
import pickle
import time
import base64
import os
import json

logger = logging.getLogger(__name__)


def generate_filename(prefix, filetype=""):
    """
    Генерирует уникальное имя файла с префиксом и временной меткой.

    Args:
        prefix (str): Префикс для имени файла (например, "users" или "config").
        filetype (str, optional): Расширение файла (например, "json" или ".txt").
            Если указано без точки, функция добавит точку автоматически. По умолчанию пустая строка.

    Returns:
        str: Уникальное имя файла с префиксом, временной меткой и расширением.
        Пример: "users_20250814_145230_123.json"
    """
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


def save_to_json(data, prefix, folder_name="json", mode="append"):
    """
    Сохраняет данные в JSON-файл в указанной папке.

    Функция автоматически создаёт папку, если она отсутствует.
    В режиме "append" создаётся новый файл с уникальным именем.
    В режиме "write" данные добавляются в существующий файл (если он есть)
    или создаётся новый файл. Поддерживаются как словари, так и списки.

    Args:
        data (dict | list): Данные для сохранения.
        prefix (str): Префикс для имени файла. Используется как основа имени файла.
        folder_name (str, optional): Имя папки для хранения файлов. По умолчанию "json".
        mode (str, optional): Режим сохранения:
            - "write" — объединяет данные с существующим файлом или создаёт новый.
            - "append" — создаёт новый файл с уникальным именем.
    """
    combined_data = data  # значение по умолчанию
    filepath = None  # чтобы не было ошибок в except

    try:
        # Путь к директории скрипта
        script_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(script_dir, folder_name)

        # Создаём папку, если нет
        os.makedirs(save_dir, exist_ok=True)

        if mode == "append":
            filename = generate_filename(prefix, "json")
            filepath = os.path.join(save_dir, filename)

        elif mode == "write":
            filename = prefix + ".json"
            filepath = os.path.join(save_dir, filename)

            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    old_data = json.load(f)

                if isinstance(old_data, dict) and isinstance(data, dict):
                    combined_data = {**old_data, **data}
                elif isinstance(old_data, list) and isinstance(data, list):
                    combined_data = old_data + data
                else:
                    combined_data = data
            else:
                combined_data = data

        else:
            raise ValueError(f"Недопустимый режим сохранения: {mode}")

        # Сохраняем данные
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, ensure_ascii=False, indent=4)
        logging.info(f"Данные успешно сохранены в файл {filepath}")

    except (IOError, OSError) as e:
        logging.error(f"Ошибка при записи файла {filepath}: {e}")
    except TypeError as e:
        logging.error(f"Ошибка сериализации данных в JSON: {e}")
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")

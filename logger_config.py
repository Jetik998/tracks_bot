import logging
import os

def setup_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Проверяем, не добавлены ли обработчики
    if not logger.handlers:

        # Файловый обработчик
        file_handler = logging.FileHandler('logs/app.log', encoding='utf-8', mode='a')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Консольный обработчик
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger

setup_logger()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import random

# --- Настройки браузера ---
options = Options()
options.add_argument("--headless")  # без отображения окна браузера
options.add_argument("--disable-blink-features=AutomationControlled")  # маскировка selenium
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

# --- Инициализация браузера ---
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- Функция поиска ---
def google_search(query):
    driver.get("https://www.google.com/")
    time.sleep(random.uniform(2, 4))  # пауза для имитации пользователя

    # Вводим запрос
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.submit()
    time.sleep(random.uniform(3, 6))

    # Собираем ссылки с результатов
    results = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")
    links = [r.get_attribute("href") for r in results]
    return links

# --- Запрос ---
query = "3 Days Later site:https://www.1001tracklists.com/"
links = google_search(query)

# --- Вывод ---
for link in links:
    print(link)

driver.quit()

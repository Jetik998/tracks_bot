from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_options = Options()
chrome_options.add_argument('--headless')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://www.1001tracklists.com')

# Немного подождать, чтобы страница загрузилась
time.sleep(2)

# Найти поле поиска — пример с использованием CSS-селектора (нужно проверить точный селектор)
search_input = driver.find_element(By.CSS_SELECTOR, 'input[type="search"]')

# Ввести текст
search_input.send_keys('Armin van Buuren')

# Отправить поиск (нажать Enter)
search_input.send_keys(Keys.RETURN)

# Подождать, чтобы загрузились результаты
time.sleep(3)

# Получить HTML результатов
html = driver.page_source

# Сохранить в файл
with open('search_results.html', 'w', encoding='utf-8') as file:
    file.write(html)

driver.quit()

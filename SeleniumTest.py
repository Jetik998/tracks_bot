import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

options = uc.ChromeOptions()
options.add_argument("--headless")  # если не нужно показывать браузер
driver = uc.Chrome(options=options)

search_url = "https://www.1001tracklists.com/search/result.php"
driver.get(search_url)
time.sleep(3)  # даем странице прогрузиться

# Заполняем форму поиска
search_box = driver.find_element("name", "main_search")
search_box.send_keys("Adam Ten & Rhye - 3 Days Later")
driver.find_element("css selector", "input[type=submit]").click()

time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

blocks = soup.select("div.bItm.oItm")
for block in blocks:
    tag = block.select_one("div.bCont.acSa > div.bTitle > a")
    if tag:
        print("Найден трек:", tag.text)

driver.quit()

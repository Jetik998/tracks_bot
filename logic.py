import requests
import random
from bs4 import BeautifulSoup
import time
import base64
from client import get_html

#time.sleep(random.uniform(1, 5))
# ЗАГОТОВКА ЧЕРЕЗ РЕКВЕСТ

def save_to_file(html, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

def captcha(url):
    image_data = url.split(",")[1]
    image_data = base64.b64decode(image_data)
    with open("captcha.jpg", "wb") as f:
        f.write(image_data)

input_track = "Adam Ten & Rhye - 3 Days Later"

payload = {
    "main_search": input_track,
    "search_selection": "2",  # 2 = поиск tracks
    "orderby": "added",
}



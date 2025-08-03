from googlesearch import search
import time
import requests
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/91.0'
]

referers = [
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://duckduckgo.com/'
]

accept_languages = [
    'en-US,en;q=0.9',
    'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'
]

headers = {
    'User-Agent': random.choice(user_agents),
    'Referer': random.choice(referers),
    'Accept-Language': random.choice(accept_languages),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
}

track = "3 Days Later (Extended Mix) Adam Ten & Rhye"

query = f'{track} site:https://www.1001tracklists.com/'
url = 'https://www.google.com/search'
params = {'q': query, 'num': '10'}

response = requests.get(url, headers=headers, params=params)
print(f'Отправленные headers: {headers}')
print('Код ответа:', response.status_code)


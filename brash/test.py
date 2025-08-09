from googlesearch import search
import time
import requests
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/91.0'
]

headers = {
    'User-Agent': random.choice(user_agents)
}


track = input(f'Напшите трек: ')
query = '{track} site:https://www.1001tracklists.com/'
count = 10
url_id = 0
url_dict = {}
for url in search(query, num_results=30):
    print(url)
    time.sleep(random.randint(5, 10))
    if url.startswith("https://www.1001tracklists.com/tracklist/"):
        url_id += 1
        url_dict[url_id] = url
        if url_id >= 10:
            break
print(url_dict)

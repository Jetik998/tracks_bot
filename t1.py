import requests

url_json = 'https://jsonplaceholder.typicode.com/todos/1'  # API, который возвращает JSON
url_html = 'https://example.com'                           # Сайт, который возвращает HTML

def check_response(url):
    response = requests.get(url)

    content_type = response.headers.get('Content-Type', '')
    print(f'URL: {url}')
    print(f'Content-Type в ответе: {content_type}')

    if 'application/json' in content_type:
        data = response.json()
        print('Это JSON! Вот данные:')
        print(data)
    else:
        print('Это не JSON. Вот текст ответа (первые 200 символов):')
        print(response.text[:200])
    print('-' * 40)

check_response(url_json)
check_response(url_html)

import requests

url_json = 'https://jsonplaceholder.typicode.com/todos/1'  # API, который возвращает JSON
url_html = 'https://example.com'                           # Сайт, который возвращает HTML

def check_response(url):
    response = requests.get(url)
    content_type = response.headers.get('Content-Type', '')
    print(f'URL: {url}')
    print(f'Content-Type в ответе: {content_type}')

    if 'application/json' in content_type:
        data = response.json()
        print('Это JSON! Вот данные:')
        print(data)
    else:
        print('Это не JSON. Вот текст ответа (первые 200 символов):')
        print(response.text[:200])
    print('-' * 40)

check_response(url_json)
check_response(url_html)

import requests

url = 'https://httpbin.org/post'  # тестовый сервис, который возвращает полученные данные
data = {
    'name': 'Иван',
    'age': 25
}

response = requests.post(url, json=data)  # отправляем POST-запрос с JSON-данными
print(response.status_code)  # код ответа сервера
print(response.json())       # сервер возвращает полученные данные в JSON

import requests

url = 'https://httpbin.org/get'
params = {
    'search': 'python',
    'page': 2
}

response = requests.get(url, params=params)
print('Фактический URL запроса:', response.url)  # посмотрим, какой URL сформировался
print(response.json())  # сервер вернёт полученные параметры

Если хочешь пройтись по разным страницам, можно в цикле менять params['page'] и делать несколько запросов:

url = 'https://httpbin.org/get'

for page in range(1, 4):  # страницы 1,2,3
    params = {'page': page}
    r = requests.get(url, params=params)
    print(r.url)  # requests сам подставил page

    """Пример отправки файла:"""

    import requests

    url = 'https://httpbin.org/post'

    files = {
        'file': open('example.txt', 'rb')  # открываем файл в бинарном режиме
    }

    response = requests.post(url, files=files)
    print(response.status_code)
    print(response.json())  # сервер покажет информацию о полученном файле

import requests

url = 'https://httpbin.org/post'

with open('example.txt', 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())


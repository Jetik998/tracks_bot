import requests

url = "https://jsonplaceholder.typicode.com/todos/1"

response = requests.get(url)
data = response.json()
print(data['title'])

import requests

session = requests.Session()
session.headers.update({'User-Agent': 'MyApp/1.0'})

url = "https://httpbin.org/headers"

response = session.get(url)
print(response.json())


import requests

url = "https://httpbin.org/basic-auth/myuser/mypass"

try:
    response = requests.get(url, auth=("myuser", "wrongpass"))
    print(response.text)
    if response.status_code == 200:
        print('Авторизация успешна')
    elif response.status_code == 401:
        print('Ошибка авторизации')
except requests.exceptions.ConnectionError:
    print('Ошибка соединения')
except requests.exceptions.Timeout:
    print("Превышен лимит ожидания от сервера")


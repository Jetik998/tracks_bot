"""Пример отправки файла:"""

import requests

url = 'https://httpbin.org/post'

files = {
    'file': open('example.txt', 'rb')  # открываем файл в бинарном режиме
}

response = requests.post(url, files=files)
print(response.status_code)
print(response.json())  # сервер покажет информацию о полученном файле

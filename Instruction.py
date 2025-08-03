#response = requests.get(url)

#response = requests.get('https://example.com')
"""Отправляет GET-запрос и получает ответ от сервера"""

#response.status_code
"""Выводит HTTP-код ответа (200 – OK, 404 – не найдено, 500 – ошибка сервера и т.д.)"""

#response.text
"""Вывести тело ответа как строку (HTML, JSON или другой текстовый формат)
Если API возвращает JSON, то в response.text будет текст с этим JSON."""

#response = requests.get('https://api.example.com/data')
#data = response.json()
"""Но чтобы удобнее работать с JSON, есть метод response.json(), который сразу превращает ответ в словарь Python."""
"""Если ответ — HTML-код, а ты вызовешь response.json(), то будет ошибка."""
"""Потому что метод .json() пытается разобрать ответ как JSON, а HTML — это не JSON."""
"""Поэтому перед вызовом .json() нужно быть уверенным, что сервер возвращает JSON."""
"""Можно проверить так"""

#if 'application/json' in response.headers.get('Content-Type', ''):
    #data = response.json()
#else:
  #  print('Ответ не в формате JSON')



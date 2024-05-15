import requests

# URL оригинальной ссылки, которую хочешь сократить
original_url = 'https://dvmn.org/modules'

# API endpoint для создания сокращенной ссылки
url = 'https://api.vk.com/method/utils.getShortLink'

# Параметры для запроса
params = {
    'v': '5.131',  # Версия API
    'url': original_url,  # URL для сокращения
    'access_token': 'd6621232d6621232d662123291d57a5c0edd662d6621232b026f18d5f6848561516b2cc'  # Твой токен доступа
}

# Выполнение GET запроса
response = requests.get(url, params=params)
response.raise_for_status()  # Проверка на ошибки в запросе

# Получение данных ответа
data = response.json()

# Вывод сокращенной ссылки
if 'response' in data:
    print("Сокращенная ссылка:", data['response']['short_url'])
else:
    print("Ошибка при создании сокращенной ссылки:", data['error']['error_msg'])

print(response.text)  # Печать всего ответа для дополнительной проверки

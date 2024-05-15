import requests


def shorten_link(token, original_url):
    url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'v': '5.131',  # Версия API
        'url': original_url,  # URL для сокращения
        'access_token': token  # Токен доступа
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # Проверка на ошибки в запросе

    data = response.json()

    if 'response' in data:
        print("Сокращенная ссылка:", data['response']['short_url'])
    else:
        print("Ошибка при создании сокращенной ссылки:", data['error']['error_msg'])


# Использование функции
if __name__ == "__main__":
    token = 'd6621232d6621232d662123291d57a5c0edd662d6621232b026f18d5f6848561516b2cc'
    original_url = input("Введите URL для сокращения: ")
    shorten_link(token, original_url)

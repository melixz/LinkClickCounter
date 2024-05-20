import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


SHORTENED_LINK_DOMAINS = ['vk.cc']


def shorten_link(token, original_url):
    url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'v': '5.131',
        'url': original_url,
        'access_token': token
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if 'response' in data:
        short_url = data['response']['short_url']
        parsed_url = urlparse(short_url)
        short_link_key = parsed_url.path.split('/')[-1]
        return short_url, short_link_key
    else:
        error_msg = data['error']['error_msg']
        raise Exception(f"Ошибка API: {error_msg}")


def count_clicks(token, short_link_key, interval='forever', intervals_count=1, extended=0):
    url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'v': '5.131',
        'key': short_link_key,
        'access_token': token,
        'interval': interval,
        'intervals_count': intervals_count,
        'extended': extended
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if 'response' in data:
        stats = data['response']['stats']
        if stats:
            for stat in stats:
                print(f"Дата начала: {stat['timestamp']}, Переходов: {stat['views']}")
        else:
            print("Статистика переходов не найдена.")
    else:
        error_msg = data['error']['error_msg']
        raise Exception(f"Ошибка API: {error_msg}")


def is_shorten_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc in SHORTENED_LINK_DOMAINS


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.environ['VK_API_TOKEN']

    original_url = input("Введите URL для сокращения: ")

    try:
        if is_shorten_link(original_url):
            print("Введена уже сокращенная ссылка:", original_url)
            short_link_key = original_url.split('/')[-1]
            count_clicks(TOKEN, short_link_key)  # Получение статистики переходов по ссылке
        else:
            short_url, short_link_key = shorten_link(TOKEN, original_url)
            print("Сокращенная ссылка:", short_url)
            count_clicks(TOKEN, short_link_key)  # Получение статистики переходов по ссылке
    except Exception as e:
        print(str(e))

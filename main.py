import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


SHORTENED_LINK_DOMAINS = ['vk.cc']


def shorten_link(token, original_url):
    api_url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'v': '5.131',
        'url': original_url,
        'access_token': token
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    response_data = response.json()

    if 'response' in response_data:
        short_url = response_data['response']['short_url']
        parsed_url = urlparse(short_url)
        short_link_key = parsed_url.path.split('/')[-1]
        return short_url, short_link_key
    else:
        error_message = response_data['error']['error_msg']
        raise Exception(f"Ошибка API: {error_message}")


def count_clicks(token, short_link_key, interval='forever', intervals_count=1, extended=0):
    api_url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'v': '5.131',
        'key': short_link_key,
        'access_token': token,
        'interval': interval,
        'intervals_count': intervals_count,
        'extended': extended
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    response_data = response.json()

    if 'response' in response_data:
        link_stats = response_data['response']['stats']
        if link_stats:
            for stat in link_stats:
                print(f"Дата начала: {stat['timestamp']}, Переходов: {stat['views']}")
        else:
            print("Статистика переходов не найдена.")
    else:
        error_message = response_data['error']['error_msg']
        raise Exception(f"Ошибка API: {error_message}")


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
            count_clicks(TOKEN, short_link_key)
        else:
            short_url, short_link_key = shorten_link(TOKEN, original_url)
            print("Сокращенная ссылка:", short_url)
            count_clicks(TOKEN, short_link_key)
    except Exception as e:
        print(str(e))

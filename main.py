import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse

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


def get_click_stats(token, short_link_key, interval='forever', intervals_count=1, extended=0):
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
        return response_data['response']['stats']
    else:
        error_message = response_data['error']['error_msg']
        raise Exception(f"Ошибка API: {error_message}")


def is_shorten_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc in SHORTENED_LINK_DOMAINS


def print_click_stats(stats):
    if stats:
        total_clicks = sum(stat['views'] for stat in stats)
        print(f"По вашей ссылке перешли {total_clicks} раз")
    else:
        print("Статистика переходов не найдена.")


if __name__ == "__main__":
    load_dotenv()
    token = os.environ.get('VK_API_TOKEN')

    if not token:
        print("Ошибка: Переменная окружения 'VK_API_TOKEN' не найдена. Пожалуйста, добавьте ее в .env файл.")
        exit(1)

    parser = argparse.ArgumentParser(
        description="Сокращение ссылок и получение статистики кликов с использованием VK API")
    parser.add_argument('url', type=str, help='URL для сокращения или уже сокращенная ссылка')
    parser.add_argument('--interval', type=str, default='forever',
                        help='Интервал для получения статистики (по умолчанию: forever)')
    parser.add_argument('--intervals_count', type=int, default=1,
                        help='Количество интервалов для получения статистики (по умолчанию: 1)')
    parser.add_argument('--extended', type=int, default=0,
                        help='Получение расширенной статистики (0 или 1, по умолчанию: 0)')

    args = parser.parse_args()
    original_url = args.url

    try:
        if is_shorten_link(original_url):
            short_link_key = original_url.split('/')[-1]
            stats = get_click_stats(token, short_link_key, args.interval, args.intervals_count, args.extended)
            print_click_stats(stats)
        else:
            short_url, short_link_key = shorten_link(token, original_url)
            print(f"{original_url} -> {short_url}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

import requests


def shorten_link(token, original_url):
    url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'v': '5.131',
        'url': original_url,
        'access_token': token
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка стандартных HTTP ошибок
        data = response.json()

        if 'error' in data:
            error_msg = data['error']['error_msg']
            raise Exception(f"Ошибка API: {error_msg}")

        return data['response']['short_url']  # Возврат короткой ссылки
    except requests.RequestException as e:
        # Обработка исключений, связанных с сетью или HTTP ответами
        raise Exception(f"Сетевая ошибка: {str(e)}")
    except Exception as e:
        # Обработка других видов ошибок, включая ошибки API
        raise Exception(f"Ошибка при сокращении ссылки: {str(e)}")


if __name__ == "__main__":
    token = 'd6621232d6621232d662123291d57a5c0edd662d6621232b026f18d5f6848561516b2cc'
    original_url = input("Введите URL для сокращения: ")
    try:
        short_link = shorten_link(token, original_url)
        print("Сокращенная ссылка:", short_link)
    except Exception as e:
        print(str(e))

import requests

url = 'https://api.vk.com/method/utils.getServerTime?v=5.131'
headers = {
    'Authorization': 'Bearer d6621232d6621232d662123291d57a5c0edd662d6621232b026f18d5f6848561516b2cc'
}
response = requests.get(url, headers=headers)
response.raise_for_status()
print(response.json())
print(response.text)
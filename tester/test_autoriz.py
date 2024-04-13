import requests

cookies = {
    'PHPSESSID': 'jeb6b049ji1v105ud3mabbslu7',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': 'PHPSESSID=jeb6b049ji1v105ud3mabbslu7',
    'origin': 'https://cafe-jojo.iikoweb.ru',
    'referer': 'https://cafe-jojo.iikoweb.ru/storeops/index.html',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

json_data = {
    'login': 'prodaji',
    'password': 'prodaji333',
}

response = requests.post('https://cafe-jojo.iikoweb.ru/api/auth/login', cookies=cookies, headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"login":"prodaji","password":"prodaji333"}'
#response = requests.post('https://cafe-jojo.iikoweb.ru/api/auth/login', cookies=cookies, headers=headers, data=data)


cookies = {
    'PHPSESSID': 'jeb6b049ji1v105ud3mabbslu7',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': '"ru_RU"',
    # 'cookie': 'PHPSESSID=jeb6b049ji1v105ud3mabbslu7',
    'referer': 'https://cafe-jojo.iikoweb.ru/storeops/index.html',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

response = requests.get('https://cafe-jojo.iikoweb.ru/api/config/get', cookies=cookies, headers=headers)


cookies = {
    'PHPSESSID': 'jeb6b049ji1v105ud3mabbslu7',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': '"ru_RU"',
    # 'cookie': 'PHPSESSID=jeb6b049ji1v105ud3mabbslu7',
    'referer': 'https://cafe-jojo.iikoweb.ru/storeops/index.html',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

response = requests.get('https://cafe-jojo.iikoweb.ru/api/stores/select/102023', cookies=cookies, headers=headers)
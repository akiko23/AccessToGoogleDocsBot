import requests, json

async def get_onetime_link(table_link):
    url = "https://cllk.ru/api/url/"
    data = {
        'url': table_link,
        'round': 2,
        'button': 0
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    return response.json()['url']


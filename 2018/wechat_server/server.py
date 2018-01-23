import requests
import json

url = 'https://mart.coding.net/api/project?'
headers = {
    'Accept': 'application/json'
}

if __name__ == '__main__':
    r = requests.get(url, headers=headers)
    with open('./data.json', 'w') as f:
        f.write(json.dumps(r.json(), ensure_ascii=False))
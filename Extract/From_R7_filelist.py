import requests
import pandas as pd
import json

# Получаем переменные
log_in = ''
pass_word = ''
url_path = ''
id_folder = ''

# Получить токен для соединения    
data = {
    "userName": log_in,
    "password": pass_word
}
endpoint = "/api/2.0/authentication.json"
url = f'{url_path}{endpoint}'
response = requests.post(url, data=data)
token = response.json()["response"]["token"]

# получаем инфо о папке
headers = {'Authorization': token}
endpoint = f'/api/2.0/files/{id_folder}'
url = f'{url_path}{endpoint}'
r = requests.get(url, headers = headers)

# экспортируем список файлов в датафрэйм
df = pd.read_json(json.dumps(r.json()['response']['files']))
df
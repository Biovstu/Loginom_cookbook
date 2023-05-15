import requests

API_TOKEN = ''
CHAT_ID = ''
ERROR_TEXT = 'Верификация пройдена!\nПривет!'
data = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={ERROR_TEXT}')
print(data)
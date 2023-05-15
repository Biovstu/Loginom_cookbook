import requests

API_TOKEN = '5788009110:AAEP5l9JHGZjn1mULk6fIQRQ0Y3dqoV0srQ'
CHAT_ID = '1012162461'
ERROR_TEXT = 'Верификация пройдена!\nПривет!'
data = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={ERROR_TEXT}')
print(data)
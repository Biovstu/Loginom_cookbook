import requests
API_TOKEN = '5332535441:AAHmyrfr4G0zsUsZpA5YuK77rl838dlIxGA'
CHAT_ID = '966221933'
ERROR_TEXT = 'helo world'
data = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={ERROR_TEXT}')
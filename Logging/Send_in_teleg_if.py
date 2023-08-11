import requests
import numpy as np, pandas as pd
import urllib.parse

input_frame = pd.DataFrame({})
    
# Здесь может быть код работы с данными
API_TOKEN = ''
CHAT_ID = ''
MESSAGE_TEXT = ''
MESSAGE_TEXT = urllib.parse.quote(MESSAGE_TEXT)
SEND_IF = ''
if input_frame.shape[0] > SEND_IF:
    data = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE_TEXT}')
import numpy as np, pandas as pd
import json
import requests
from requests.auth import HTTPBasicAuth

input_frame = pd.DataFrame({})

LOGIN = ''
PASSWORD = ''
ODATASERVER = ''

# Здесь может быть код работы с данными
basic = HTTPBasicAuth(LOGIN.encode('utf-8'), PASSWORD.encode('utf-8'))
refs = 'Period,Валюта_Key,Валюта____Presentation,Курс,Кратность'
buff_resp = requests.get(f"{ODATASERVER}/InformationRegister_КурсыВалют?$select={refs}", headers=dict(Accept='application/json;odata=nometadata'), auth=basic)
curents = pd.read_json(json.dumps(buff_resp.json()['value']))

curents['Date'] = curents.Period.astype('datetime64[ns]')
cur = []
mult = []

for i,key in enumerate(input_frame['Валюта_Key']):
    temp = curents.loc[(curents['Date'] <= input_frame.loc[i,'Date']) & (curents['Валюта_Key'] == key), ['Date', 'Курс', 'Кратность']]
    temp = temp[(temp['Date'] == temp['Date'].max())]
    cur.append(temp['Курс'].max())
    mult.append(temp['Кратность'].max())

input_frame['Курс'] = cur
input_frame['Кратность'] = mult

# Полученный выходной pd.DataFrame
output_frame = input_frame
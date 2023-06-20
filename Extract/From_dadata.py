import numpy as np
import pandas as pd
import json
import requests
from requests.auth import HTTPBasicAuth

LOGIN = ''
PASSWORD = ''
ODATASERVER = ''
# Здесь может быть код работы с данными
basic = HTTPBasicAuth(LOGIN.encode('utf-8'), PASSWORD.encode('utf-8'))
refs = 'Ref_Key,Description'
buff_resp = requests.get(f"{ODATASERVER}/Catalog_СегментыНоменклатуры?$select={refs}", headers=dict(Accept='application/json;odata=nometadata'), auth=basic)
buff_df = pd.read_json(json.dumps(buff_resp.json()['value']))

from dadata import Dadata

import time

token = ''
secret = ''

with Dadata(token, secret) as dadata:
    for i,adres in enumerate(buff_df['Представление']):
        if i % 1000 == 0:
            print(f'{i} - {adres}')
        try:
            js = dadata.clean(name='address', source=adres)
        except RemoteProtocolError:
            time.sleep(30)
            js = dadata.clean(name='address', source=adres)
        except ReadTimeout:
            time.sleep(30)
            js = dadata.clean(name='address', source=adres)
        except ConnectTimeout:
            time.sleep(30)
            js = dadata.clean(name='address', source=adres)
        try:
            df = pd.DataFrame(js, index=[0])
        except ValueError:
            df = pd.DataFrame(js).head(1)
        df['Ref_Key'] = buff_df.loc[i,'Ref_Key']
        if i == 0:
            output_frame = df
        else:
            output_frame = pd.concat([output_frame,df], ignore_index=True)
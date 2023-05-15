import numpy as np
import pandas as pd
import json
import requests
from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth('odata_erp'.encode('utf-8'), 'oeLrXMT1Eryp9YM9P8st'.encode('utf-8'))
refs = 'Ref_Key,Description'
buff_resp = requests.get(f"http://dcr-iis03/erp_data/odata/standard.odata/Catalog_СегментыНоменклатуры?$select={refs}", headers=dict(Accept='application/json;odata=nometadata'), auth=basic)
buff_df = pd.read_json(json.dumps(buff_resp.json()['value']))

from dadata import Dadata

token = "1a92df4e58672fe394d72da001c6022a90936540"
secret = "ebca67c1e0b63922f82f07b51ce149cea4850e25"

with Dadata(token, secret) as dadata:
    for i,adres in enumerate(download_data['Представление']):
#         print(f'{i} - {adres}')
        js = dadata.clean(name='address', source=adres)
        try:
            df = pd.DataFrame(js, index=[0])
        except ValueError:
            df = pd.DataFrame(js).head(1)
        df['Ref_Key'] = download_data.loc[i,'Ref_Key']
        if i == 0:
            output_frame = df
        else:
            output_frame = pd.concat([output_frame,df], ignore_index=True)
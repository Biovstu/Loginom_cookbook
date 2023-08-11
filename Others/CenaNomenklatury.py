import numpy as np
import pandas as pd
import json
import requests
from requests.auth import HTTPBasicAuth
import time

t = time.strftime('%X', time.localtime(time.time()))
print(f'{t} - Начнем!')
# формируем аутентификацию
basic = HTTPBasicAuth(''.encode('utf-8'), ''.encode('utf-8'))
# делаем запрос OData
buff_resp = requests.get(f"http://dcr-iis03/erp_data/odata/standard.odata/InformationRegister_ЦеныНоменклатурыПоставщиков", headers=dict(Accept='application/json;odata=nometadata'), auth=basic)
t = time.strftime('%X', time.localtime(time.time()))
print(f'{t} - Ответ получен: {buff_resp}')
# Читаем полученый JSON в Pandas
download_data = pd.read_json(json.dumps(buff_resp.json()['value']))

# функция по исправлению некорректной JSON строки
def tru_js(string):
    return str(string).replace("'",'"').replace(': ',':').replace('[','').replace(']','').replace('True','true').replace('False','false')

# Добавляем столбец с корректной JSON строкой
download_data['Correct record'] = download_data['RecordSet'].apply(tru_js)
# Формируем пустую выходную таблицу со столбцами из вложенных JSON
col = pd.read_json(download_data.loc[0, 'Correct record'], lines=True)
col['Recorder'] = download_data.loc[0, 'Recorder']
col.drop(col.index, inplace=True)

# Читаем основую таблицу построчно, раскрываем JSON и добавляем в выходну таблицу
for rec in download_data.index:
    col_tmp = pd.read_json(download_data.loc[rec, 'Correct record'], lines=True)
    col_tmp['Recorder'] = download_data.loc[rec, 'Recorder']
    col = pd.concat([col, col_tmp],ignore_index=True)
    if rec % 1000 == 0:
        t = time.strftime('%X', time.localtime(time.time()))
        print(f'{t} - Раскрываю запись №{rec}')
t = time.strftime('%X', time.localtime(time.time()))
print(f'{t} - Готово! {rec} записей раскрыто.')

file_path = 'Z:\\Для логистов и закупок\\'
# file_path = 'C:\\ProgramData\\BaseGroup\\Loginom 6\\Server\\UserStorage\\konstantin.kutovoy\\Ежеквартальное планирование'
# Записываем результат в файл
col.to_csv(file_path+'CenaNomenklaturyPostavschikov.csv', encoding='cp1251')
print('Файл записан')

# Шлем радостную весть
API_TOKEN = ''
CHAT_ID = ''
ERROR_TEXT = 'Регистра Цены номенклатуры выгружен!'
data = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={ERROR_TEXT}')
print(data)
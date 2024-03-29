import numpy as np, pandas as pd

# Импорт специализированных библиотек для испорта из Р7
import requests
import shutil
import tempfile
import os
import openpyxl
import datetime

# Получаем переменные
log_in = ''
pass_word = ''
url_path = ''
id_file = ''
file_name = ''
list_list = ''
rename = ''

#поэлементное чтение входных таблиц в список из DataFrame
input_frames = [pd.DataFrame({})]

# Получить токен для соединения    
data = {
    "userName": log_in,
    "password": pass_word
}
endpoint = "/api/2.0/authentication.json"
url = f'{url_path}{endpoint}'
response = requests.post(url, data=data)
token = response.json()["response"]["token"]

tmp_path = 'C:\\ProgramData\\BaseGroup\\Loginom 6\\Server\\UserStorage\\service\\temp\\'+file_name+'.xlsx'

if list_list.count(',') >= 1:
    list_list = list_list.split(',')
else:
    lst = list_list
    list_list = []
    list_list.append(lst)

# экспорт во многостраничный документ эксель
with pd.ExcelWriter(tmp_path) as writer:
    for i, frame in enumerate(input_frames):
        if i < len(list_list):
            frame.to_excel(writer, sheet_name=list_list[i])
        else:
            frame.to_excel(writer, sheet_name=f'Лист{i+1}')

'''
# экспорт во многостраничный документ с распределением по листам
with pd.ExcelWriter(tmp_path) as writer:
    for i in list_list:
        frame = input_frame[input_frame['Заказчик'] == i]
        frame.to_excel(writer, sheet_name=i)
'''

# отправляем файл
with open(tmp_path,'rb') as f:
    file = {'file': f}
    data = {'fileExtension': 'xlsx'}
    headers = {'Authorization': token}
    endpoint = f'/api/2.0/files/{id_file}/update'
    url = f'{url_path}{endpoint}'
    r = requests.put(url, data=data, files=file, headers = headers)

# удаляем файл
os.remove(tmp_path)

# переименовываем файл, если надо
if rename:
    data = {'title': file_name}
    headers = {'Authorization': token}
    endpoint = f'/api/2.0/files/file/{id_file}'
    url = f'{url_path}{endpoint}'
    r = requests.put(url, data=data, headers = headers)

# Записываем результат и реквизиты файла
output_frame = pd.read_json(r.text).reset_index()

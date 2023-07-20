import pandas as pd
import time

t = time.strftime('%X', time.localtime(time.time()))
print(f'{t} - Начнем!')

download_data = pd.DataFrame({})

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

file_path = ''
file_name = ''
# Записываем результат в файл
col.to_csv(file_path+file_name+'.csv', encoding='cp1251')
print('Файл записан')

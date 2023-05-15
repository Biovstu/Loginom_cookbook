import numpy as np, pandas as pd

#поэлементное чтение входных таблиц в список из DataFrame
input_frames = [pd.DataFrame({})]

# Получаем путь к файлу
file_path = ''
# Получаем имя файла без расширения
file_name = ''
list_list = ''

if list_list.count(',') > 1:
    list_list = list_list.split(',')
else:
    list_list = list(list_list)
# экспорт во многостраничный документ эксель
with pd.ExcelWriter(file_path) as writer:
    for i, frame in enumerate(input_frames):
        if i < len(list_list):
            frame.to_excel(writer, sheet_name=list_list[i])
        else:
            frame.to_excel(writer, sheet_name=f'Лист{i+1}')

# Записываем результат и реквизиты файла
print(f'Результат: Успешно\nПуть к файлу: {file_path}\nИмя файла: {file_name}+.xlsx')
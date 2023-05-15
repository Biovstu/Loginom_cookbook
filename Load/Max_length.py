import numpy as np, pandas as pd

#копируем из буферной DataFrame во входную, при этом названия столбцов тянем из Входной таблицы
input_frame = pd.DataFrame({})

max_values = {}

def len_x(value):
    value = str(value).replace('None','')
    return len(value)
    
# проверяем каждый столбец, если в нем тип даннх строковый (object), то создаем новый столбец с примененной функций очистки
for i in input_frame.columns:
    if input_frame[i].dtype == 'object':
        max_values[i] = []
        max_values[i].append(input_frame[i].apply(len_x).max())

# создаем выходной набор
output_frame = pd.DataFrame(max_values)
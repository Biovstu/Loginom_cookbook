import numpy as np, pandas as pd

#копируем из буферной DataFrame во входную, при этом названия столбцов тянем из Входной таблицы
input_frame = pd.DataFrame({})

# функция для преобразования
def get_idrref(refkey):
    if refkey.count('-') == 4:
        refkey = refkey.split('-')
        return refkey[3]+refkey[4]+refkey[2]+refkey[1]+refkey[0]
    else:
        return refkey

# создаем пустой выходной набор
output_frame = pd.DataFrame({})

# проверяем настройки: столбцы добавляем?
suffix = '' # суффикс
adding = '' # Добавляем столбцы?
fields = ''.split(',') # поля

# проверяем каждый столбец, если в нем тип даннх строковый (object), то создаем новый столбец с примененной функций очистки
for i in input_frame.columns:
    if input_frame[i].name in fields:
        if adding: # если добавляем, то копируем исходный столбец и добавляем новый с суффиксом и с очищенными значениями
            output_frame[i] = input_frame[i]
            output_frame[i + suffix] = input_frame[i].apply(get_idrref)
        else: # если нет, то добавляем только новый столбец со старым именем и с очищенными значениями
            output_frame[i] = input_frame[i].apply(get_idrref)
    else:# не текстовые столбцы просто копируем
        output_frame[i] = input_frame[i]
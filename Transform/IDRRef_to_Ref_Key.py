import numpy as np, pandas as pd

#копируем из буферной DataFrame во входную, при этом названия столбцов тянем из Входной таблицы
input_frame = pd.DataFrame({})

# функция очистки от известных непечатных символов и удаления множества пробелов подряд
def get_refkey(idrref):
    return idrref[24:]+'-'+idrref[20:24]+'-'+idrref[16:20]+'-'+idrref[:4]+'-'+idrref[4:16]

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
            output_frame[i + suffix] = input_frame[i].apply(get_refkey)
        else: # если нет, то добавляем только новый столбец со старым именем и с очищенными значениями
            output_frame[i] = input_frame[i].apply(get_refkey)
    else:# не текстовые столбцы просто копируем
        output_frame[i] = input_frame[i]
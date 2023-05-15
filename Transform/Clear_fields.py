import numpy as np, pandas as pd

#копируем из буферной DataFrame во входную, при этом названия столбцов тянем из Входной таблицы
input_frame = pd.DataFrame({})

# функция очистки от известных непечатных символов и удаления множества пробелов подряд
def total_clear(field_data):
    field_data = str(field_data).replace('None','')
    if field_data != '':
        field_data = field_data.replace('\f',' ').replace('\n',' ').replace('\r',' ').replace('\t',' ').replace('\v',' ').replace('  ',' ')
        if '  ' in field_data:
            field_data = total_clear(field_data)
    return field_data.strip()

# создаем пустой выходной набор
output_frame = pd.DataFrame({})

# проверяем настройки: столбцы добавляем?
suffix = '' # суффикс
adding = '' # Добавляем столбцы?
fields = ''.split(',') # поля


# проверяем каждый столбец, если в нем тип даннх строковый (object), то создаем новый столбец с примененной функций очистки
for i in input_frame.columns:
    if input_frame[i].dtype == 'object' and input_frame[i].name in fields:
        if adding: # если добавляем, то копируем исходный столбец и добавляем новый с суффиксом и с очищенными значениями
            output_frame[i] = input_frame[i]
            output_frame[i + suffix] = input_frame[i].apply(total_clear)
        else: # если нет, то добавляем только новый столбец со старым именем и с очищенными значениями
            output_frame[i] = input_frame[i].apply(total_clear)
    else:# не текстовые столбцы просто копируем
        output_frame[i] = input_frame[i]
import numpy as np, pandas as pd

input_frame = pd.DataFrame({})

# проверяем настройки: названия столбцов РТУ и ВВ
col_nom = '' # столбец с номенклатурой
col_qty = '' # столбец с количеством
buffer_frame = pd.pivot_table(input_frame, values=col_qty, index=col_nom, aggfunc=np.sum).reset_index()
buffer_frame.columns = ['Номенклатура_Key','Заказано MAX']
zakazy = []
for key in buffer_frame[col_nom]:
    zakazy.append(', '.join(list(input_frame[input_frame[col_nom] == key]['Number'])))
buffer_frame['Заказ клиента'] = zakazy
output_frame = buffer_frame
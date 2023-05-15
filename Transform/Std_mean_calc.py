import numpy as np, pandas as pd

input_frame = pd.DataFrame({})

# проверяем настройки: названия столбцов РТУ и ВВ
col_nom = '' # столбец с номенклатурой
col_qty = '' # столбец с количеством
buffer_frame = pd.pivot_table(input_frame, values=col_qty, index=col_nom, aggfunc=[np.std, np.mean]).reset_index()
buffer_frame.columns = ['Номенклатура_Key','std','mean']

output_frame = buffer_frame
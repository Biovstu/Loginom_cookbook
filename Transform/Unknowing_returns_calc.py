import numpy as np, pandas as pd

input_frame = pd.DataFrame({})

# проверяем настройки: названия столбцов РТУ и ВВ
col_rtu = '' # столбец РТУ
col_vv = '' # столбец ВВ
col_finrtu = '' # столбец Итоговых РТУ

output_frame = pd.DataFrame({})

for j,col in enumerate(input_frame['Номенклатура_Key'].unique()):
    vv_cumulative = []
    should_return = []
    buffer_frame = input_frame[input_frame['Номенклатура_Key'] == col].reset_index(drop=True)
    for i in range(len(buffer_frame[col_rtu])):
        if i == 0:
            vv_cumulative.append(buffer_frame[col_vv][i])
        else:
            vv_cumulative.append(buffer_frame[col_vv][i] + vv_cumulative[i-1] - should_return[i-1])
        if vv_cumulative[i] >= buffer_frame[col_rtu][i]:
            should_return.append(buffer_frame[col_rtu][i])
        else:
            should_return.append(vv_cumulative[i])
    buffer_frame[col_finrtu] = buffer_frame[col_rtu] - pd.Series(should_return)
    if j == 0:
        output_frame = buffer_frame
    else:
        output_frame = pd.concat([output_frame, buffer_frame], ignore_index=True)
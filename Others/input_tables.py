import builtin_data
from builtin_data import InputTable, InputTables, InputVariables, OutputTable, DataType, DataKind, UsageType
import numpy as np, pandas as pd
from builtin_pandas_utils import to_data_frame, prepare_compatible_table, fill_table

# Входной порт необязательный
if InputTable:
    # Создать pd.DataFrame по входному набору №1
    buffer_frame = to_data_frame(InputTable)

#копируем из буферной DataFrame во входную, при этом названия столбцов тянем из Входной таблицы
input_frame = pd.DataFrame({})
for num_col,col in enumerate(InputTable.Columns):
    input_frame[col.DisplayName] = buffer_frame[buffer_frame.columns[num_col]]

#поэлементное чтение входных таблиц в список из DataFrame
input_frames = []
for num_table, table in enumerate(InputTables):
    if table:
        # Создать pd.DataFrame по входному набору №1
        buffer_frame = to_data_frame(table)
    #копируем из буферной DataFrame во входную, при этом названия столбцов тянем из Входной таблицы
    input_frames.append(pd.DataFrame({}))
    for num_col, col in enumerate(table.Columns):
        input_frames[num_table][col.DisplayName] = buffer_frame[buffer_frame.columns[num_col]]
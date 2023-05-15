import builtin_data
from builtin_data import InputTable, InputTables, InputVariables, OutputTable, DataType, DataKind, UsageType
import numpy as np, pandas as pd
from builtin_pandas_utils import to_data_frame, prepare_compatible_table, fill_table

# Если включена опция "Разрешить формировать выходные столбцы из кода", структуру выходного набора можно подготовить по pd.DataFrame
if isinstance(OutputTable, builtin_data.ConfigurableOutputTableClass):
    prepare_compatible_table(OutputTable, output_frame, with_index=False)

# Транслитерированные на этапе подготовки названия столбцов переименовываем обратно в исходные
for num_col,col in enumerate(OutputTable.Columns): 
    col.DisplayName = output_frame.columns[num_col]
    
fill_table(OutputTable, output_frame, with_index=False)
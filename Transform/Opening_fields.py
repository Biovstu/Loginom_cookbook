import numpy as np, pandas as pd

#копируем из буферной DataFrame во входную, при этом названия столбцов тянем из Входной таблицы
input_frame = pd.DataFrame({})

# Здесь может быть код работы с данными
for ind,req in enumerate(input_frame['ТНВЭД']):
    if req.count(',') == 0:
        if ind == 0:
            df_export = pd.DataFrame({'Наименование':[input_frame['Наименование'][ind]],'ТНВЭД':[input_frame['ТНВЭД'][ind]]})
        else:
            df_export = pd.concat([df_export,pd.DataFrame({'Наименование':[input_frame['Наименование'][ind]],'ТНВЭД':[input_frame['ТНВЭД'][ind]]})],ignore_index=True)
    while req.count(',') >= 1:
        i = req.find(',')
        if ind == 0:
            df_export = pd.DataFrame({'Наименование':[input_frame['Наименование'][ind]],'ТНВЭД':[req[:i]]})
        else:
            df_export = pd.concat([df_export,pd.DataFrame({'Наименование':[input_frame['Наименование'][ind]],'ТНВЭД':[req[:i]]})],ignore_index=True)
        req = req[i+1:]
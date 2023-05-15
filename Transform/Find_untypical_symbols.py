import numpy as np, pandas as pd
import re

input_frame = pd.DataFrame({})

# проверяем настройки:
field = '' # название поля для поиска

# создаем словарь с упоминанием всех символов, которые не являеются буквами или цифрами
d = {}
for i,string in enumerate(input_frame[field]):
    symbols = re.findall(r'\W',string)
    for c in symbols:
        lab = f'"{c}":char({ord(c)})'
        d.setdefault(lab,[input_frame.loc[i,'Ref_Key']])
        d[lab].append(input_frame.loc[i,'Ref_Key'])

# записываем словарь в таблицу
output_frame = pd.DataFrame.from_dict(d, orient='index').T
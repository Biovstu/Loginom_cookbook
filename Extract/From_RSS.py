import pandas as pd

list_df = pd.read_html('https://www.cbr.ru/currency_base/daily/',thousands=' ', decimal=',')

print(list_df[0])

from_alta = pd.read_html('https://www.alta.ru/tnved/forbidden_codes/')
print(from_alta)

for d in from_alta:
    if d.shape[1] == 5:
        tnved = d
print(tnved)
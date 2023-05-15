import numpy as np, pandas as pd

input_frames = [pd.DataFrame({})]

df = input_frames[0]
mask = list(input_frames[1]['ТНВЭД короткий'])
print(mask)

def inlist(field):
    i = 0
    succes = False
    serching = True
    while serching:
        if mask[i] in field:
            succes = (field.find(mask[i]) == 0)
            serching = not succes
        else:
            serching = not (i == (len(mask) - 1))
        i += 1
    return succes

# Здесь может быть код работы с данными
if len(mask) > 0:
    df['есть в списке'] = df['ТНВЭД'].apply(inlist)
else:
    df['есть в списке'] = False

output_frame = df
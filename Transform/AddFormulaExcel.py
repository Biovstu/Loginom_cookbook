import pandas as pd

input_frame = pd.DataFrame({})

new_column_name = ''
mask = ''
new_column = []
for i in input_frame.index:
    new_column.append(mask.replace('#',f'{i+2}'))
input_frame[new_column_name] = new_column
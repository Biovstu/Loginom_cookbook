import pandas as pd

input_frame = pd.DataFrame({})

output_frame = pd.DataFrame({})

ref_key = input_frame['Ref_Key'].unique()

for key in ref_key:
    df_of_key = input_frame.loc[input_frame['Ref_Key'] == key, ['Ref_Key','Квартал','Calendar','Дней','PotrebnostQTY']].reset_index(drop=True)
    quarter = df_of_key['Квартал'].unique()
    for q in quarter:
        daily_qty = []
        df_of_quarter = df_of_key.loc[df_of_key['Квартал'] == q, ['Ref_Key','Квартал','Calendar','Дней','PotrebnostQTY']].reset_index(drop=True)
        for i in df_of_quarter.index:
            qty = round((df_of_quarter.loc[i, 'PotrebnostQTY'] - sum(daily_qty)) / (df_of_quarter.loc[i, 'Дней'] - i), 0)
            daily_qty.append(qty)
        df_of_quarter['daily_qty'] = daily_qty
        if output_frame.shape[0] == 0:
            output_frame = df_of_quarter
        else:
            output_frame = pd.concat([output_frame, df_of_quarter], ignore_index=True)

print(output_frame)
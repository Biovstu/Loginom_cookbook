import pandas as pd

start_date = ''
if start_date == '':
    start_date = None
end_date = ''
if end_date == '':
    end_date = None
freq_date = ''
if freq_date == '':
    freq_date = 'D'
periods = 0
if start_date is None or end_date is None:
    if periods == 0:
        periods = 1
else:
    periods = None
name = ''
if name == '':
    name = 'Calendar'

output_frame = pd.DataFrame(pd.date_range(start=start_date, end=end_date, periods=periods, freq=freq_date, name=name))
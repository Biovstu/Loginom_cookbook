import numpy as np, pandas as pd

input_frame = pd.DataFrame({})

output_frame = pd.DataFrame(input_frame.nunique()).reset_index()

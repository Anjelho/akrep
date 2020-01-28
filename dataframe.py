import pandas as pd
raw = 'import.csv'
x = pd.read_csv(raw, delimiter='|')
print(x)
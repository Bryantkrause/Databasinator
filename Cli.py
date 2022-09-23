import pandas as pd

file = r'C:\Users\bkrause\Documents\Data.xls'
df = pd.read_excel(file)

print(df.head())
print(df.shape)
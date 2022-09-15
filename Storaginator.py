from genericpath import isfile
import queries
import config
import pandas as pd
import subprocess
import os
from pathlib import Path


data = []
query = queries.location()
file = 'Location.xlsx'
directory = Path('C:/Users/bkrause/Documents/CodeMe/Databasinator/Location.xlsx')
openizer = r'C:\Users\bkrause\Documents\CodeMe\Databasinator\Location.xlsx'
config.cursor.execute(query)
for row in config.cursor:
    row_to_list = [elem for elem in row]
    data.append(row_to_list)
columnHeaders = [column[0] for column in config.cursor.description]

df = pd.DataFrame(data)
df.columns = columnHeaders
location = df
# print(df.head())
# print(df.info())
# print(df.describe())

writer = pd.ExcelWriter(file, engine='xlsxwriter')
location.to_excel(writer, sheet_name='Location')
writer.close()

if directory.is_file():
    print('File exists')
    os.system(openizer)
else:
    print('file does not exist')

import queries
import config
import pandas as pd
import psutil
import subprocess

data = []
query = queries.location()


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

writer = pd.ExcelWriter('Location.xlsx', engine='xlsxwriter')
location.to_excel(writer, sheet_name='Location')
writer.save()

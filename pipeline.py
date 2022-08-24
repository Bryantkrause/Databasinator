import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
import queries

data = []

# get connection data
load_dotenv('.env')
DSN =os.environ.get("DSN")
UID =os.environ.get("UID")
PWD =os.environ.get("PWD")

# establish connection
conn = pyodbc.connect(f'DSN={DSN};UID={UID};PWD={PWD}')

# test connection
cursor = conn.cursor()

cursor.execute(queries.palletsRec())

for i in cursor:
    data.append(i)

print(data)

df = pd.DataFrame(data)
print(df)

writer = pd.ExcelWriter('PalletsRecieved.xlsx', engine='xlsxwriter')

df.to_excel(writer, sheet_name='PalletsRecieved')

writer.save()
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
# set connection
cursor = conn.cursor()
# run query
cursor.execute(queries.storageByUnit())
# convert raw data to list format
for  row in cursor:
    row_to_list = [elem for elem in row]
    data.append(row_to_list)  
# add data to data frame
# df = pd.DataFrame(data, columns=['Number','Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
df = pd.DataFrame(data)
# write excel file
writer = pd.ExcelWriter('Storage.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='PalletsRecieved')
writer.save()
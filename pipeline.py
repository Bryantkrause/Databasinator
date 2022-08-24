import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
import queries

# get connection data
load_dotenv('.env')
DSN =os.environ.get("DSN")
UID =os.environ.get("UID")
PWD =os.environ.get("PWD")

# establish connection
conn = pyodbc.connect(f'DSN={DSN};UID={UID};PWD={PWD}')

# test connection
cursor = conn.cursor()
# print(queries.palletsRec())
cursor.execute(queries.palletsRec())
for i in cursor:
    print(i)

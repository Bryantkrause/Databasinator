import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os

# get connection data
load_dotenv('.env')
DSN =os.environ.get("DSN")
UID =os.environ.get("UID")
PWD =os.environ.get("PWD")

# establish connection
conn = pyodbc.connect(f'DSN={DSN};UID={UID};PWD={PWD}')

# test connection
cursor = conn.cursor()
cursor.execute('SELECT * FROM customer')
for i in cursor:
    print(i)

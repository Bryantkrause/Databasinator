import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
import queries


# get connection data
load_dotenv('.env')
DSN = os.environ.get("DSN")
UID = os.environ.get("UID")
PWD = os.environ.get("PWD")

# establish connection
conn = pyodbc.connect(f'DSN={DSN};UID={UID};PWD={PWD}')
# set connection
cursor = conn.cursor()
# run query


# get report name to run
# query = str(input("Enter Report:"))
query = 'unloadPal'
# pass required query
def runQuery(query):
    print(query)



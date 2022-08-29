import Display.TableWithDataFrame as Table
import queries
import config
import pandas as pd


palletsInData = []

config.cursor.execute(queries.unloadPalletized())
for row in config.cursor:
    row_to_list = [elem for elem in row]
    palletsInData.append(row_to_list)
df = pd.DataFrame(palletsInData)

print(df)

Table.table_example(df)


import Display.TableWithDataFrame as Table
import queries
import config
import pandas as pd

palletsInData = []
Inboundinator = [queries.unloadPalletized(), queries.upTo1T(), queries.lz1T(), queries.lz3T(), queries.lz2T3T(),
                 queries.lz1T2T(), queries.unload20(), queries.unload40(), queries.unload45(), queries.lz1000(), queries.M2T(), queries.UnldUnit(), queries.EAAway(), queries.UnldUnitAll(), queries.SrtConfirmM(), queries.SrtConfirm(), queries.SrtConfirm5(), queries.InLabelCase(), queries.palletPutaway()]

chargeName = ['unloadpallet', 'upTo1T', 'lz1T']
allList = []
data = []

for query in Inboundinator:
    config.cursor.execute(query)
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        data.append(row_to_list)


df = pd.DataFrame(data)
df.columns = ['Key', 'Charge', 'Date', 'AMT']
df.set_index('Key')
print(df)
# pivotar = df.pivot_table(values='AMT',columns='Charge',index=['Date',[df.index.values,'Key']], fill_value=0, sort=True).reset_index('Key')
pivotar = df.pivot_table(values='AMT', columns='Charge', index=[
                         'Date', 'Key'], fill_value=0, sort=True).reset_index()

# config.cursor.execute(queries.AllInbound())
# for row in config.cursor:
#     row_to_list = [elem for elem in row]
#     palletsInData.append(row_to_list)
# df = pd.DataFrame(palletsInData)
# df.columns = ['Customer','Order', 'Date', 'Facility', 'Method','Qty','Laden','Pallets']
# df['Key'] = df['Customer'].astype(str) + df['Facility']
# df = df[['Key']+[col for col in df.columns if col != 'Key']]
# df.set_index('Key')

Table.table_example(pivotar)

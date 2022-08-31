from cmath import pi
import Display.TableWithDataFrame as Table
import queries
import config
import pandas as pd

palletsInData = []
Inboundinator = [queries.unloadPalletized(), queries.upTo1T(), queries.lz1T(), queries.lz3T(), queries.lz2T3T(), queries.Between1T2T(),
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
df.columns = ['ID','Key', 'Charge', 'Date', 'AMT']
df.set_index('Key')
print(df)
# pivotar = df.pivot_table(values='AMT',columns='Charge',index=['Date',[df.index.values,'Key']], fill_value=0, sort=True).reset_index('Key')
pivotar = df.pivot_table(values='AMT', columns='Charge', index=[
                         'Date', 'ID', 'Key'], fill_value=0, sort=True).reset_index()
print(pivotar.columns)

Unload = ['FloorLoad Up to: 1000', 'FloorLoad Pieces:1001-2000 ',
          'LZ 1001-2000', 'LZ 2001-3000', 'LZ > 1000', 'LZ<1000', 'LZ> 3000',
          'UNLD 20 FT FLR CNT', 'UNLD 40 FT FLR CNT', 'UNLD 45 FT FLR CNT',
          'UNLD PLTZD', 'UNLD UNIT', 'UNLD UNIT ALL']
Putaway = ['EA PUTAWAY', 'PLT PUTAWAY']
Labeling = ['IN LABELING CS']
SortAndConf = ['SORT & CONFIRM', 'SORT & CONFIRM 5+', ]
totals = ['Unloading', 'Putaway', 'Sorting', 'Labeling']
summaraized = ['Date', 'Key', 'ID',  'Unloading',
               'Putaway', 'Sorting', 'Labeling', 'Total']

pivotar['Unloading'] = pivotar[Unload].sum(axis=1)
pivotar['Putaway'] = pivotar[Putaway].sum(axis=1)
pivotar['Sorting'] = pivotar[SortAndConf].sum(axis=1)
pivotar['Labeling'] = pivotar[Labeling].sum(axis=1)
pivotar['Total'] = pivotar[totals].sum(axis=1)
Summary = pivotar[summaraized]
Summary = Summary.round(2)

print(Summary.info)
print(Summary.dtypes)
print(Summary.shape)
print(Summary.memory_usage)
# checker for 0 in unloading
# pivotar = pivotar.loc[pivotar['Unloading'] == 0]


# Table.table_example(Summary)
writer = pd.ExcelWriter('MonthlySummary.xlsx', engine='xlsxwriter')
Summary.to_excel(writer, sheet_name='Summary')
pivotar.to_excel(writer, sheet_name='Raw')
writer.save()

import pipeline
import queries
import pandas as pd


storageData = []
palletsInData = []

pipeline.runQuery(pipeline.query)
# run storage report
if pipeline.query == 'storage':
    print('running storage report')
    pipeline.cursor.execute(queries.storageByUnit())
    for  row in pipeline.cursor:
        row_to_list = [elem for elem in row]
        storageData.append(row_to_list)
    df = pd.DataFrame(storageData)
    df.columns = ['Name', 'Date', 'Type', 'QTY']
    df['Type'] = df['Type'].replace([1,2,3],['Receive','Ship','Adj'])
    storagePivot = df.pivot_table(columns=['Type'],index=['Name', 'Date'],  values=['QTY'])
    storagePivot['Monthly Total'] = storagePivot.sum(axis=1, numeric_only=True).cumsum()
    writer = pd.ExcelWriter('Storage.xlsx', engine='xlsxwriter')
    storagePivot.to_excel(writer, sheet_name='StorageByUnit')
    writer.save()


# run pallets recieved report
elif pipeline.query == 'palletsIn':
    print('running pallets recieved report')
    pipeline.cursor.execute(queries.palletsRec())
    for  row in pipeline.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData, columns=['Number', 'Year', 'Jan', 'Feb', 'Mar',
                      'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    writer = pd.ExcelWriter('PalletsIn.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='PalletsRecieved')
    writer.save()
# if choice is invalid notify user
else:
    print('that is not an option at this time')


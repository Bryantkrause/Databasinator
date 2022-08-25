import pipeline
import queries
import pandas as pd
import smtplib

storageData = []
palletsInData = []

pipeline.runQuery(pipeline.query)
# run storage report
if pipeline.query == 'storage':
    print('running storage report')
    pipeline.cursor.execute(queries.storageByUnit())
    for row in pipeline.cursor:
        row_to_list = [elem for elem in row]
        storageData.append(row_to_list)
    df = pd.DataFrame(storageData)
    df.columns = ['Name', 'Date', 'Type', 'QTY']
    df['Type'] = df['Type'].replace([1, 2, 3], ['Receive', 'Ship', 'Adj'])
    storagePivot = df.pivot_table(columns=['Type'], index=[
                                  'Name', 'Date'],  values=['QTY'])
    storagePivot['Monthly Total'] = storagePivot.sum(
        axis=1, numeric_only=True).cumsum()
    lRow = len(storagePivot.index) + 2
    Col = len(storagePivot.columns) + 1
    SRow = 3
    writer = pd.ExcelWriter('Storage.xlsx', engine='xlsxwriter')
    storagePivot.to_excel(writer, sheet_name='StorageByUnit')
    workbook = writer.book
    worksheet = writer.sheets['StorageByUnit']
    chart = workbook.add_chart({'type': 'line'})
    chart.add_series({
        'name': 'Monthly Total',
        'categories': ['StorageByUnit', SRow, Col-4, lRow, Col-4],
        'values': ['StorageByUnit', SRow, Col, lRow, Col],
        'data_labels': {'value': True},
    })
    chart.set_x_axis({'name': 'Date', 'position_axis': 'on_tick'})
    chart.set_y_axis({'name': 'Units', 'major_gridlines': {'visible': False}})
    chart.set_legend({'none': True})
    worksheet.insert_chart('I2', chart,{'x_scale': 2, 'y_scale': 1})
    writer.save()

# run pallets recieved report
elif pipeline.query == 'palletsIn':
    print('running pallets recieved report')
    pipeline.cursor.execute(queries.palletsRec())
    for row in pipeline.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData, columns=['Number', 'Year', 'Jan', 'Feb', 'Mar',
                      'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    writer = pd.ExcelWriter('PalletsIn.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='PalletsRecieved')
    writer.save()
#  run inbound accesorials 
elif pipeline.query == 'inAcc':
    print('running inbound accessorial report with criteria')
    pipeline.cursor.execute(queries.inAcc())
    for row in pipeline.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('InAcc.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='InAcc')
    writer.save()
#  run inbound tariffs
elif pipeline.query == 'inTar':
    print('running inbound tariff report with criteria')
    pipeline.cursor.execute(queries.inTar())
    for row in pipeline.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('InTar.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='InTar')
    writer.save()
#  run unload palletized charges report
elif pipeline.query == 'unloadPal':
    print('running unloading palletized with charges')
    pipeline.cursor.execute(queries.unloadPalletized())
    for row in pipeline.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('unloadPalletized.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='unloadPalletized')
    writer.save()
#  run unload palletized charges report
elif pipeline.query == 'lz1000':
    print('running unloading cartons less than 1000 report')
    pipeline.cursor.execute(queries.lz1000())
    for row in pipeline.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('lz1000.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='lz1000')
    writer.save()
# if choice is invalid notify user
else:
    print('that is not an option at this time')

import config
import queries
import pandas as pd
import smtplib

storageData = []
palletsInData = []
query = 'storage'
config.runQuery(query)
# run storage report
if query == 'storage':
    print('running storage report')
    config.cursor.execute(queries.storageByUnit())
    for row in config.cursor:
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
    worksheet.insert_chart('I2', chart, {'x_scale': 2, 'y_scale': 1})
    writer.save()

# run pallets recieved report
elif query == 'palletsIn':
    print('running pallets recieved report')
    config.cursor.execute(queries.palletsRec())
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData, columns=['Number', 'Year', 'Jan', 'Feb', 'Mar',
                      'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    writer = pd.ExcelWriter('PalletsIn.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='PalletsRecieved')
    writer.save()
#  run inbound accesorials
elif query == 'inAcc':
    print('running inbound accessorial report with criteria')
    config.cursor.execute(queries.inAcc())
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('InAcc.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='InAcc')
    writer.save()
#  run inbound tariffs
elif query == 'inTar':
    print('running inbound tariff report with criteria')
    config.cursor.execute(queries.inTar())
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('InTar.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='InTar')
    writer.save()
#  run unload palletized charges report
elif query == 'unloadPal':
    print('running unloading palletized with charges')
    config.cursor.execute(queries.unloadPalletized())
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('unloadPalletized.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='unloadPalletized')
    writer.save()
#  run unload palletized charges report
elif query == 'lz1000':
    print('running unloading cartons less than 1000 report')
    config.cursor.execute(queries.lz1000())
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('lz1000.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='lz1000')
    writer.save()
#  run unload cartons between 1001 and 2000
elif query == 'lz1T2T':
    print('running unloading cartons great than 1000 but less than 2000 report')
    config.cursor.execute(queries.lz1T2T())
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('lz1T2T.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='lz1T2T')
    writer.save()
#  run unload cartons between 2001 and 3000
elif query == 'lz2T3T':
    print('running unloading cartons great than 2000 but less than 3000 report')
    config.cursor.execute(queries.lz2T3T())
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('lz2T3T.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='lz2T3T')
    writer.save()
#  run unload cartons greater 3000
elif query == 'lz3T':
    print('running unloading cartons greater than 3000 report')
    config.cursor.execute(queries.lz3T())
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('lz3T.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='lz3T')
    writer.save()
#  run unload cartons greater 1000
elif query == 'lz1T':
    print('running unloading cartons greater than 1000 report')
    config.cursor.execute(queries.lz1T())
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('lz1T.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='lz1T')
    writer.save()
#  run unload cartons up to 1000
elif query == 'upTo1T':
    print('running unloading cartons greater than 1000 report')
    config.cursor.execute(queries.upTo1T())
    for row in config.cursor:
        row_to_list = [elem for elem in row]
        palletsInData.append(row_to_list)
    df = pd.DataFrame(palletsInData)
    writer = pd.ExcelWriter('upTo1T.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='upTo1T')
    writer.save()
# if choice is invalid notify user
else:
    print('that is not an option at this time')

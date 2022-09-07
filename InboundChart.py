from cmath import pi
import Display.TableWithDataFrame as Table
import queries
import config
import pandas as pd
import main

ch = main.dfChart
rows = len(main.dfChart)-1
number = len(ch.columns)-1
print(ch)
for x in range(rows):
    print(x+2, number)

# writer = pd.ExcelWriter('MonthlySummary.xlsx', engine='xlsxwriter')
# workbook = writer.book
# worksheet = writer.sheets['charty']
# chart = workbook.add_chart({'type': 'line'})

# chart.add_series({
#     'name': 'Monthly Total',
#     'categories': ['StorageByUnit', SRow, Col-4, lRow, Col-4],
#     'values': ['StorageByUnit', SRow, Col, lRow, Col],
#     'data_labels': {'value': True},
# })

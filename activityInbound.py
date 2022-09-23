import sys
import ActivityQueries
import config
import pandas as pd

data = []
# run inbound pallet report and put into data frame
config.cursor.execute(ActivityQueries.inboundPallets())
for row in config.cursor:
    row_to_list = [elem for elem in row]
    data.append(row_to_list)

df = pd.DataFrame(data)

# update column headers to word not number
df.columns = ['ID','Location','Jan','Feb',
'Mar','Apr','May','Jun','Jul',
'Aug','Sep','Oct','Nov','Dec']
# columns to be totaled
col_list = ['Jan', 'Feb',
            'Mar', 'Apr', 'May', 'Jun', 'Jul',
            'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# replace NAN and None with 0
df.fillna(0,inplace=True)
# replace index with customer number
df['Key'] = df['ID'].astype(str) + df['Location']
df.set_index('Key', inplace=True)
# add total column
df['Total'] = df[col_list].sum(axis=1)
df.sort_values(by='Total', ascending=False, inplace=True)
print(df.head())
print(df.describe())
print(df.info())
# removed inactive customers
df2 = df.drop(["402FULLERTON", "428FULLERTON", "137CERRITOS","137FULLERTON", "412CERRITOS", "415FULLERTON", "409FULLERTON", "403FULLERTON"])

df2 = df2.loc[:, (df2 != 0).any(axis=0)]


newCol = list(df2.columns)
listEnd = len(newCol)-1
newCol = newCol[2:listEnd]

# ['ID', 'Location', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Total']
df2['Ave'] = df2[newCol].mean(axis=1)

# create % column
df2['%'] = df2['Total'] / df2['Total'].sum()


# add total row this should be last before entering into Excel
df2.loc['Total'] = df2.sum(numeric_only=True)
# put data into excel
writer = pd.ExcelWriter('Activity.xlsx', engine='xlsxwriter')
df2.to_excel(writer, sheet_name='InboundPallets')
writer.close()
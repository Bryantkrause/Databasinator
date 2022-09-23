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
df.columns = ['ID','Jan','Feb',
'Mar','Apr','May','Jun','Jul',
'Aug','Sep','Oct','Nov','Dec']
col_list = ['Jan', 'Feb',
            'Mar', 'Apr', 'May', 'Jun', 'Jul',
            'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df.fillna(0,inplace=True)

df['Total'] = df[col_list].sum(axis=1)
df.sort_values(by='Total', ascending=False, inplace=True)
print(df.head())
print(df.describe())
print(df.info())

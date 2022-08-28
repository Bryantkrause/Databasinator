import PySimpleGUI as sg
import pandas as pd


df = pd.DataFrame({
    'date': ['5/1/2017', '5/2/2017', '5/3/2017', '5/1/2017', '5/2/2017', '5/3/2017', '5/1/2017', '5/2/2017', '5/3/2017'],
    'city': ['ny', 'ny', 'ny', 'muble', 'muble', 'muble', 'bejin', 'bejin', 'bejin', ],
    'temp': [65, 66, 68, 75, 78, 82, 80, 77, 79],
    'humidity': [56, 58, 60, 80, 83, 85, 26, 30, 35]
})

def table_example():

    if not df.empty:
        try:
            # Header=None means you directly pass the columns names to the dataframe
            data = df.values.tolist()               # read everything else into a list of rows
                                # Press if you named your columns in the csv
                # Uses the first row (which should be column names) as columns names
            header_list = df.columns.tolist()
                # Drops the first row in the table (otherwise the header names and the first row will be the same)
            data = df[0:].values.tolist()
        except:
            sg.popup_error('Missing Data')
            return

    layout = [
        [sg.Table(values=data,
                  headings=header_list,
                  display_row_numbers=True,
                  auto_size_columns=False,
                  num_rows=min(25, len(data)))]
    ]

    window = sg.Window('Table', layout, grab_anywhere=False)
    event, values = window.read()
    window.close()


table_example()

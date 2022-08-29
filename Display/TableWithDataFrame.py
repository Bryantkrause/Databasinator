import PySimpleGUI as sg
import pandas as pd
import sys


sg.theme("DarkBlue")
def table_example(df):

    if not df.empty:
        try:
            data = df.values.tolist()               
            header_list = df.columns.tolist()
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




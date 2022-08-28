# import PySimpleGUI as sg

# sg.theme('DarkAmber')    # Keep things interesting for your users

# layout = [[sg.Text('Persistent window')],
#           [sg.Input(key='-IN-')],
#           [sg.Button('Read'), sg.Exit()]]

# window = sg.Window('Window that stays open', layout)

# while True:                             # The Event Loop
#     event, values = window.read()
#     print(event, values)
#     if event == sg.WIN_CLOSED or event == 'Exit':
#         break

# window.close()

import PySimpleGUI as sg

sg.theme('DarkBlue')

layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Show'), sg.Button('Exit')]]

window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

window.close()

# import PySimpleGUI as sg

# sg.preview_all_look_and_feel_themes()

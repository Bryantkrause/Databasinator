import PySimpleGUI as sg

layout = [[sg.Text('My one-shot window.')],
          [sg.InputText(key='-IN-')],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('Window Title', layout)

event, values = window.read()
window.close()

text_input = values['-IN-']
print(text_input)
sg.popup('You entered', text_input)

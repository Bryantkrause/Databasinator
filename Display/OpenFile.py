import PySimpleGUI as sg
import sys

if len(sys.argv) == 1:
    fname = sg.popup_get_file('Document to open')
else:
    fname = sys.argv[1]

if not fname:
    sg.popup("Cancel", "No filename supplied")
    raise SystemExit("Cancelling: no filename supplied")
else:
    sg.popup('The filename you chose was', fname)

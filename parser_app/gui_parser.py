import PySimpleGUI as sg
import layout_elements
from parse_s7 import *
from display_file import *


window = layout_elements.make_window()
window['-ADD KEY-'].set_cursor(cursor='hand2')
window['-REMOVE KEY-'].set_cursor(cursor='hand2')
window['-FILE LIST-'].set_cursor(cursor='hand2')
window['-REMOVE FILE-'].set_cursor(cursor='hand2')
window['-CLEAR FILES-'].set_cursor(cursor='hand2')
window['-CLEAR FILES-'].set_cursor(cursor='hand2')
# Run the Event Loop
file_list =[]
disp_list = []
keys = []
while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
   
    if event == "-FILE-":
        f = values["-FILE-"]
        disp_list.append(f.split('/')[-1].strip('.txt'))
        file_list.append(f)
        window["-FILE LIST-"].update(disp_list)
    elif event == "-REMOVE FILE-":
        try:
            f_remove = values['-FILE LIST-'][0]
            disp_list.remove(f_remove)
            file_list = [f for f in file_list if f_remove not in f]
        except:
            pass
        window["-FILE LIST-"].update(disp_list)
    elif event == "-ADD KEY-":
        if values["-KEY-"].strip() != '':
            keys.append(values["-KEY-"])
        window["-KEY-"]('')
        window["-KEY LIST-"].update(keys)
    elif event == "-REMOVE KEY-":
        try:
            key_remove = values["-KEY LIST-"][0]
            keys.remove(key_remove)
        except:
            pass
        window["-KEY LIST-"].update(keys)
    elif event == "-CLEAR FILES-":
        file_list, disp_list = [],[]
        window["-FILE-"]('')
        window["-FILE LIST-"].update(disp_list)
    elif event == "-CLEAR KEYS-":
        keys = []
        window["-KEY-"]('')
        window["-KEY LIST-"].update(keys)
    elif event == '-PARSE-':
        full_display(None, None)
        for i,f in enumerate(file_list):
            begin_audit(f,keys,disp_list[i])
            window['-PARSED FILE SELECT-'].update(values =disp_list)
            
    elif event == '-PARSED FILE SELECT-':
        print('pepe')
       
       

window.close()
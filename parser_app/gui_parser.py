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
audit_path ={}
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
        clear_stuff(["-FILE-",'-FILE LIST-'],window)

    elif event == "-CLEAR KEYS-":
        keys = []
        clear_stuff(["-KEY-",'-KEY LIST-'],window)

    elif event == '-PARSE-':
        if len(keys)>0:
            for i,f in enumerate(file_list):
                audit_path[str(disp_list[i])] = begin_audit(f,keys,disp_list[i])
            window['-PARSED FILE SELECT-'].update(values =disp_list)  
            window['-PARSED FILE SELECT SEARCHABLE-'].update(values =disp_list)
            enable_stuff(['-PARSED FILE SELECT-','-PARSED FILE SELECT EXPANDABLE-',
                        '-PARSED FILE SELECT SEARCHABLE-', '-PARSED LAC SELECT SEARCHABLE-',
                        '-PARSED CONVEYOR SELECT SEARCHABLE-',],window)

    elif event == '-PARSED FILE SELECT-':
        path = audit_path[values['-PARSED FILE SELECT-']]
        window['-FULL OUTPUT-'].update('')
        full_display(path,window)

    elif event == '-CLEAR FULL OUTPUT-':
        window['-FULL OUTPUT-'].update('')

    elif event == '-PARSED FILE SELECT SEARCHABLE-':
        path = audit_path[values['-PARSED FILE SELECT SEARCHABLE-']]
        load_LACs(path, window)

    elif event =='-PARSED LAC SELECT SEARCHABLE-':
        path = audit_path[values['-PARSED FILE SELECT SEARCHABLE-']]
        LAC = values['-PARSED LAC SELECT SEARCHABLE-']
        load_conveyors(path, LAC, window)

    elif event == '-SEARCH SEARCHABLE OUTPUT-':
        if not values['-MULTI SEARCH CB-']:
            clear_stuff(['-SEARCHABLE OUTPUT-'],window)
        path = audit_path[values['-PARSED FILE SELECT SEARCHABLE-']]
        LAC = values['-PARSED LAC SELECT SEARCHABLE-']
        conveyor = values['-PARSED CONVEYOR SELECT SEARCHABLE-']
        searchable_display(path,LAC, conveyor,window)

    elif event == '-CLEAR SEARCHABLE OUTPUT-':
        clear_stuff(['-SEARCHABLE OUTPUT-','-PARSED LAC SELECT SEARCHABLE-',
                     '-PARSED LAC SELECT SEARCHABLE-','-PARSED CONVEYOR SELECT SEARCHABLE-'],window)

    elif event == '-DISPLAY TAB-':
        stuff = ['-SEARCHABLE OUTPUT-','-FULL OUTPUT-','-PARSED LAC SELECT SEARCHABLE-',
                '-PARSED LAC SELECT SEARCHABLE-', '-PARSED CONVEYOR SELECT SEARCHABLE-',
                '-EXPANDABLE OUTPUT-','-PARSED FILE SELECT SEARCHABLE-','-PARSED FILE SELECT-']
        clear_stuff(stuff,window)
        
    
window.close()
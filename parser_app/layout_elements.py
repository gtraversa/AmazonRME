from tkinter.constants import S
import PySimpleGUI as sg
def make_window(full_combo_values = []):
    sg.theme('DarkBlack1')
    file_list_column = [
        [
            sg.Text("Select File"),
            sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse(file_types=(('Text Files', '*.txt'),)),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 5), key="-FILE LIST-"
            )

        ],
        [
            sg.Button(
                button_text='Remove', key="-REMOVE FILE-"
            ),
            sg.Button(
                button_text='Clear', key="-CLEAR FILES-"
            )
        ],
    ]


    keyword_list_column = [
        [
            sg.Text('Enter keyword to filter'),
            sg.In(size=(25, 1), enable_events=True, key="-KEY-"),
            sg.Button(button_text='Add', key="-ADD KEY-"),

        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 5), key="-KEY LIST-"
            ),
            sg.Button(
                button_text='Parse', key='-PARSE-', size=(5, 3)
            ),
        ],
        [
            sg.Button(
                button_text='Remove', key="-REMOVE KEY-"
            ),
            sg.Button(
                button_text='Clear', key="-CLEAR KEYS-"
            ),

        ],
    ]


    full_display_column = [
        [
            sg.Output(
               size=(40, 6), key='-FULL OUTPUT-'
            ),
        ],
        [
            sg.Text('Select file'),
            sg.Combo(values=full_combo_values,auto_size_text = True, enable_events=True, key='-PARSED FILE SELECT-')
        ],
    ]



    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(keyword_list_column),
            sg.VSeparator(),
            sg.TabGroup([[
                sg.Tab('Full', full_display_column)
            ]]),
        ]
    ]
    return sg.Window("S7 Parser", layout,finalize=True)

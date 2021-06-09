from os import write
from tkinter.constants import S
import PySimpleGUI as sg
def make_window():
    sg.theme('DarkBlack1')
    file_list_column = [
        [
            sg.Text("Select File"),
            sg.In(size=(40, 1), enable_events=True, key="-FILE-"),
            sg.FileBrowse(file_types=(('Text Files', '*.txt'),)),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(55, 5), key="-FILE LIST-"
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
            sg.In(size=(40, 1), enable_events=True, key="-KEY-"),
            sg.Button(button_text='Add', key="-ADD KEY-"),

        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(58, 5), key="-KEY LIST-"
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
    selection_full_display = [
        [
            sg.Text('Select file'),
        ],
        [
            sg.Combo(values=[],
            auto_size_text = True,
            enable_events=True, 
            disabled = True,
            key='-PARSED FILE SELECT-'
            ),
        ],
        [
            sg.Button(button_text = 'Clear',key = '-CLEAR FULL OUTPUT-')
        ],
    ]

    selection_expandable_display = [
        [
            sg.Text('Select file'),
        ],
        [
            sg.Combo(values=[],
            auto_size_text = True,
            enable_events=True, 
            disabled = True,
            key='-PARSED FILE SELECT EXPANDABLE-'
            ),
        ],
        [
            sg.Button(button_text = 'Clear',key = '-CLEAR EXPANDABLE OUTPUT-')
        ],
    ]

    selection_searchable_display = [
        [
            sg.Text('Select file'),
        ],
        [
            sg.Combo(values=[],
            auto_size_text = True,
            enable_events=True, 
            disabled = True,
            key='-PARSED FILE SELECT SEARCHABLE-'
            ),
        ],
        [
            sg.Text('Select LAC'),
        ],
        [
            sg.Combo(values=[],
            auto_size_text = True,
            enable_events=True, 
            disabled = True,
            key='-PARSED LAC SELECT SEARCHABLE-'
            ),
        ],
        [
            sg.Text('Select conveyor'),
        ],
        [
            sg.Combo(values=[],
            auto_size_text = True,
            enable_events=True, 
            disabled = True,
            key='-PARSED CONVEYOR SELECT SEARCHABLE-'
            ),
        ],
        [
            sg.Button(button_text = 'Search',key = '-SEARCH SEARCHABLE OUTPUT-'),
            sg.Checkbox('Keep previous searches', default=False, k='-MULTI SEARCH CB-'),
        ],
        [
            sg.Button(button_text = 'Clear',key = '-CLEAR SEARCHABLE OUTPUT-')
        ],
    ]


    full_display = [
        [
            sg.Multiline(
               size=(90, 20), 
               key='-FULL OUTPUT-',
               disabled=True
            ),
            sg.Column(selection_full_display,vertical_alignment = 'top'),
        ],
    ]

    expandable_display = [
        [
            sg.Listbox(
               size=(90, 19), 
               key='-EXPANDABLE OUTPUT-',
               values=[]
            ),
            sg.Column(selection_expandable_display,vertical_alignment = 'top'),
        ],

    ]

    searchable_display = [
        [
            sg.Multiline(
               size=(90, 20), 
               key='-SEARCHABLE OUTPUT-',
               disabled = True
            ),
            sg.Column(selection_searchable_display,vertical_alignment = 'top'),
        ],
    ]



    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(keyword_list_column) 
        ],
        [sg.TabGroup([[
                        sg.Tab('Full', full_display),
                        sg.Tab('Expandable', expandable_display),
                        sg.Tab('Searchable', searchable_display)
                    ]],enable_events=True,key = '-DISPLAY TAB-', size = (950,335)),
                    
        ],


    ]
    return sg.Window("S7 Parser", layout,finalize=True)

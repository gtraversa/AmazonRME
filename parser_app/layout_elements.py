import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import ThisRow

def make_window():
    sg.theme('DarkBlack1')
    file_list_column = [
        [
            sg.Text("Select File"),
            sg.In(size=(40, 1), key="-FILE-"),
            sg.FileBrowse(file_types=(('Text Files', '*.txt'),)),
            sg.Button(button_text = 'Add', enable_events=True, key = '-ADD FILE-')
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(64, 5), key="-FILE LIST-"
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
            sg.Button(button_text='All with keyword',key = '-ALL KW-', enable_events = True),
            sg.Button(button_text='All without keyword',key = '-ALL NO KW-',enable_events = True),
            sg.Button(button_text = 'Clear',key = '-CLEAR FULL OUTPUT-')
        ],
        [
            sg.Multiline(
               size=(20, 5), 
               key='-KEYS DISPLAY-',
               disabled=True
            ),
            sg.Button(button_text = 'Extract keys', enable_events= True, key ='-EXTRACT KEYS-')
        ]
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
            sg.Button(button_text = 'Clear',key = '-CLEAR EXPANDABLE OUTPUT-'),
            sg.Button(button_text = 'Collapse', key = '-COLLAPSE EXPANDABLE OUTPUT-')
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
            sg.Checkbox('All', default= False, k = '-ALL CONV CB-', enable_events = True),
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
               values=[],
               enable_events= True
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

    parsing_input = [[
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(keyword_list_column),
    ]]

    parsed_input = [
            [
            sg.Text("Select File"),
            sg.In(size=(110, 1), key="-JSON FILE-"),
            sg.FileBrowse(button_text ='File',file_types=(('Text Files', '*.json'),)),
            sg.FolderBrowse(button_text ='Folder', target = (ThisRow,-2)),
            sg.Button(button_text = 'Add', enable_events=True, key = '-ADD PARSED-')
            ],
            [
            sg.Listbox(
                values=[], 
                enable_events=True, 
                size=(100, 5), 
                key="-FILE LIST LOAD-",
                pad = ((80,5),(0,5))
            ), 
            sg.Button(
                button_text='Load', key='-LOAD-', size=(5, 3)
            ),

            ],
            [
                sg.Button(
                    button_text='Remove', key="-REMOVE FILE LOAD-",pad = ((80,0),(0,0))
                ),
                sg.Button(
                    button_text='Clear', key="-CLEAR FILES LOAD-"
                )
            ],
    ]


    layout = [
        [sg.TabGroup([[
                        sg.Tab('Parse New',parsing_input),
                        sg.Tab('Load', parsed_input),
        ]])
        ],
        [sg.TabGroup([[
                        sg.Tab('Full', full_display),
                        sg.Tab('Expandable', expandable_display),
                        sg.Tab('Searchable', searchable_display)
                    ]],enable_events=True,key = '-DISPLAY TAB-', size = (1000,335)),
                    
        ],
        [
            sg.Text('Created by Gianluca Traversa (RME Intern), Joe Rush and Jessica Lucas © 2021.',
            tooltip='Source Code',
            enable_events = True,
            font = ('Helvetica',7),
            text_color='Gray',
            key = '-COPYRIGHT-'),
        ]

    ]
    return sg.Window("S7 Parser", layout,finalize=True)

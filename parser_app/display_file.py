import PySimpleGUI as sg
import json

def full_display(path,window):
    try:
        with open(path) as jfile:
            f = json.load(jfile)
            for lac in f.keys():
                for conv in f[lac]:
                    try:
                        del f[lac][conv]['load_identity']
                    except:
                        pass
            window['-FULL OUTPUT-'].print(json.dumps(f, indent = 4).replace('"','').replace('\\',''))
            window['-FULL OUTPUT-'].get()#TODO this is to get elements
    except Exception as e:
        window['-FULL OUTPUT-'].print(e)

def load_LACs(path,window):
    try:
        with open(path) as jfile:
            f = json.load(jfile)
            lacs = []
            for lac in f.keys():
                lacs.append(lac)
            window['-PARSED LAC SELECT SEARCHABLE-'].update(values = lacs)
    except Exception as e:
        window['-SEARCHABLE OUTPUT-'].print(e)

def load_conveyors(path,LAC,window):
    try:
        with open(path) as jfile:
            f = json.load(jfile)
            convs = []
            for conv in f[LAC].keys():
                convs.append(conv)
            window['-PARSED CONVEYOR SELECT SEARCHABLE-'].update(values = convs)
    except Exception as e:
        window['-SEARCHABLE OUTPUT-'].print(e)

def searchable_display(path,LAC,conveyor,window):
    try:
        with open(path) as jfile:
            f = json.load(jfile)[LAC][conveyor]
            del f['load_identity']
            window['-SEARCHABLE OUTPUT-'].print(conveyor+json.dumps(f, indent = 4).replace('"','').replace('\\',''))
    except Exception as e:
        print(e)


def expandable_display():
    pass

def get_combos(path):
    pass

def clear_stuff(stuff,window):
    for thing in stuff:
        window[thing].update('')

def enable_stuff(stuff, window):
    for thing in stuff:
        window[thing].update(disabled = False)

def disable_stuff(stuff, window):
    for thing in stuff:
        window[thing].update(disabled = True)

#IX_ResetESM QX_TrspStopped
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
    except Exception as e:
        window['-FULL OUTPUT-'].print(e)

def load_LACs(path,window):
    try:
        with open(path) as jfile:
            f = json.load(jfile)
            lacs = []
            for lac in f.keys():
                lacs.append(lac)
            update_values_stuff(['-PARSED LAC SELECT SEARCHABLE-'],lacs,window)
    except Exception as e:
        window['-SEARCHABLE OUTPUT-'].print(e)

def load_conveyors(path,LAC,window):
    try:
        with open(path) as jfile:
            f = json.load(jfile)
            convs = []
            for conv in f[LAC].keys():
                convs.append(conv)
            update_values_stuff(['-PARSED CONVEYOR SELECT SEARCHABLE-'],convs,window)
    except Exception as e:
        window['-SEARCHABLE OUTPUT-'].print(e)

def searchable_display(path,LAC,conveyor,window,values):
    try:
        with open(path) as jfile:
            if values['-ALL CONV CB-']:
                f = json.load(jfile)[LAC]
                for conv in f.keys():
                    del f[conv]['load_identity']
                    window['-SEARCHABLE OUTPUT-'].print(conv+json.dumps(f[conv], indent = 4).replace('"','').replace('\\',''))
            else:
                f = json.load(jfile)[LAC][conveyor]
                del f['load_identity']
                window['-SEARCHABLE OUTPUT-'].print(conveyor+json.dumps(f, indent = 4).replace('"','').replace('\\',''))
    except Exception as e:
        print(e)


def expandable_display(path,depth,window,expanded_keys,target = [None]):
    try:
        if target[0] in expanded_keys and target[0] is not None:
            expanded_keys.remove(target[0])
            expandable_display(path,depth,window,expanded_keys)
            expanded_keys.remove(None)
            return expanded_keys
        with open(path) as jfile:
            expanded_keys.append(target[0])
            f = json.load(jfile)
            if depth == 0:
                update_values_stuff(['-EXPANDABLE OUTPUT-'],[lac for lac in f.keys()],window)       
            elif depth == 1:
                vals = []
                for lac in f.keys():
                    vals.append(lac)
                    if target[0] in f[lac].keys() or lac in expanded_keys:
                        for conv in f[lac].keys():
                            vals.append('       ->' + conv)
                            if '       ->' + conv == target[0] or conv in [key.strip().strip('->') for key in expanded_keys if key is not None]:
                                del f[lac][conv]['load_identity']
                                for key in f[lac][conv].keys():
                                    vals.append('                ->' + key + ' : ' +f[lac][conv][key])
                               
                update_values_stuff(['-EXPANDABLE OUTPUT-'],vals,window)
        return expanded_keys
    except Exception as e:
        print(e)
   
def clear_stuff(stuff,window):
    for thing in stuff:
        window[thing].update('')

def enable_stuff(stuff, window):
    for thing in stuff:
        window[thing].update(disabled = False)

def disable_stuff(stuff, window):
    for thing in stuff:
        window[thing].update(disabled = True)

def update_values_stuff(stuff,values,window):
    for thing in stuff:
        window[thing].update(values = values)

def remove_duplicates(lst):
    return list(dict.fromkeys(lst))
#IX_ResetESM QX_TrspStopped
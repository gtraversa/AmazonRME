import PySimpleGUI as sg
import json

def full_display(path):
    try:
        with open(path) as jfile:
            f = json.load(jfile)
            print(json.dumps(f, indent = 3,))#print(json.dumps(parsed, indent = 2))
    except Exception as e:
        print(e)

def partial_display(path,LAC,conveyor):
    pass

def get_combos(path):
    pass

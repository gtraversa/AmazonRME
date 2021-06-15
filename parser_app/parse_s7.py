import copy

import os
import json
from exception_print import *

def audit_file(f, keys, exact):
    """ Parse .txt s7 file and extract desired features
    
        @param f: File currently being parsed
        @type f: File
        @param keys: ID list of parameters to parse from the file (add any number)
        @type keys: List[Str]
    """
    full_data = {}
    data = {}
    assign = None
    load = None
    long_assign = []
    long_assign_flg = False
    conv_num = None
    LAC_num = None
    parameters = generate_parameter_dict(keys)
    for line in f:
        if 'TITLE' in line:
            if 'LAC' in line:
                data = {}
                LAC_num = line.split('=')[1].split('-')[0].strip()
                full_data[LAC_num] = data
            else:
                conv_num = line.split('=')[1].strip()
                if len(line.split('-')) != 2:
                    conv_num = None
                elif 'Conveyor' not in conv_num:
                    conv_num = None
                else:
                    data[conv_num] = copy.deepcopy(parameters)
    
        if conv_num is not None:
            if ' A' in line:
                assign = line.strip().strip('A;').strip()
            if ' = ' in line:
                load = line.split('=')[1].strip().strip('L;').strip()
                if long_assign_flg:
                    data[conv_num]['load_identity'][load]=long_assign[:-1]
                    long_assign = []
                    long_assign_flg = False
                    load = None
                    assign = None
            if long_assign_flg:
                long_assign.append(line.strip().strip(';'))

            if 'A(' in line:
                long_assign_flg = True
            
            if load is not None and assign is not None:
                data[conv_num]['load_identity'][load]=assign.strip('"')
                load= None
                assign = None

            if 'CALL' in line:
                data[conv_num]['Conveyor_model'] = line.split('_')[0].split('"')[1]+line.split('_')[1]
            for param in parameters.keys():
                search_word = ''
                if exact:
                    search_word = ' ' + param + ' '
                    if search_word in line:
                        if ':= L' in line:
                            load = line.split(':=')[1].strip().strip('L').strip(' L,);').strip()
                            assign = data[conv_num]['load_identity'][load]
                            try:
                                data[conv_num][param] = assign.strip('"')
                            except:
                                data[conv_num][param] = assign
                            load, assign = None, None
                        else:
                            data[conv_num][param] = line.split(':=')[1].strip(',').strip().strip(',')
                else:
                    search_word = param
                    if search_word in line:
                        if ':= L' in line:
                            load = line.split(':=')[1].strip().strip('L').strip(' L,);').strip()
                            assign = data[conv_num]['load_identity'][load]
                            parameter = line.split(':=')[0].strip()
                            try:
                                data[conv_num][parameter] = assign.strip('"')
                            except:
                                data[conv_num][parameter] = assign
                            load, assign = None, None
                        else:
                            try:
                                data[conv_num][parameter] = line.split(':=')[1].strip(',').strip().strip(',')
                            except:
                                 data[conv_num][parameter] = '?'
    full_data[LAC_num] = data
    return full_data


def generate_parameter_dict(keys):
        """ Generate dictionary storing and identifying parameters

            @param keys: ID list of parameters to parse from the file (add any number)
            @type keys: List[Str]
        """
        parameters = {'load_identity':{},'Conveyor_model':''}
        for key in keys:
                parameters[key]= ''
        return parameters

def begin_audit(f, keys,save_name,exact):
    """ Basic validity check of file path and call parsing function, returns the path to the parsed .json

        @param f: Path to .txt file to be parsed
        @type f: Str
        @param keys: ID list of parameters to parse from the file (add any number)
        @type keys: List[Str]
        @param save_name: Name to save the parsed .json file as
        @type save_name: Str
        @param exact: True if the exact keyword is to be searched, False if a line containing the word is to be searched
        @type exact: Bool
    """
    try:
        data = audit_file(open(f,'r'),keys, exact)
    except Exception as e:
        PrintException()
        return 'Error'
    key_string= ''
    file_name = ''
    for key in keys:
        key_string += str(key) +'-'
    sep = '/'
    if exact:
        folder_path =  sep.join(f.split('/')[:-1]).strip("[']")+'/'+str(key_string).strip('-')+'_Exact'
        file_name = folder_path+'/'+save_name+'_exact_parsed.json'
    else:
        folder_path =  sep.join(f.split('/')[:-1]).strip("[']")+'/'+str(key_string).strip('-')
        file_name = folder_path+'/'+save_name+'_parsed.json'
    os.makedirs(folder_path,exist_ok=True)
    with open(file_name,'w') as finish:
        finish.write(json.dumps(data, indent = 1))
    return file_name

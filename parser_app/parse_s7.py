import copy
import os
import json
from exception_print import *

def audit_file_regular(f, keys, exact):
    """ Parse old .txt s7 file and extract desired features
    
        @param f: File currently being parsed
        @type f: File
        @param keys: ID list of parameters to parse from the file (add any number)
        @type keys: List[Str]
    """
    full_data = {}
    data = {}
    assign = []
    load = None
    long_assign = []
    long_assign_flg = False
    norm_assign_flg = False
    conv_num = None
    LAC_num = None
    bad_word_check_list = [ 'interface','Latch','JAM','End','SAV','Baler','>',
                        '<','Jam', 'Induct','BALER','Blade','Operating','MAC',
                        'Disable','split','available','Merge','Function',
                        'Interface','Cognex','Send','Prepare','Divert',
                        'Point','Scanning','Lock','Position','Profile','Profinet',
                        'Mapping','SCADA','Accel','Diagnostic','Windows',
                        'waiting','Inward']
    good_word_check_list = [ 'MT Conveyor Module','Belt Conveyor Module',
                            'ACC Conveyor Module','KDR ACC Module','KDR MT Module',
                            'TBT Module','Spiral Conveyor Module','Spiral Control Module',
                            'Belt Curve Module']
    parameters = generate_parameter_dict(keys)
    for line in f:
        if 'TITLE' in line:
            if 'TITLE =LAC' in line:
                data = {}
                LAC_num = line.split('=')[1]
                full_data[LAC_num] = data
            elif any(word in line  for word in good_word_check_list) and 'SEW' not in line:
                conv_num = line.split('=')[1].strip()
                data[conv_num] = copy.deepcopy(parameters)
            else:
                conv_num = None
        
        if conv_num is not None:
            if ' A ' in line and not long_assign_flg:
                assign.append(line.strip().strip(';'))
                norm_assign_flg = True
            elif ' AN' in line and not long_assign_flg:
                assign.append(line.strip().strip(';'))
                norm_assign_flg = True
            elif ' O' in line and not long_assign_flg:
                assign.append(line.strip().strip(';'))
                norm_assign_flg = True
            elif ' ON' in line and not long_assign_flg:
                assign.append(line.strip().strip(';'))
                norm_assign_flg = True
            if ' = ' in line:
                load = line.split('=')[1].strip().strip('=L;').strip()
                if norm_assign_flg:
                    if long_assign_flg:
                        assign.append(long_assign)
                        long_assign_flg = False
                        long_assign = []
                    data[conv_num]['load_identity'][load]=assign
                    assign = []
                    norm_assign_flg = False
                    load = False
                    
            if long_assign_flg:
                long_assign.append(line.strip().strip(';'))

            if 'A(' in line:
                long_assign.append('A(')
                long_assign_flg = True
                norm_assign_flg = True

            if 'O(' in line:
                long_assign.append('O(')
                long_assign_flg = True
                norm_assign_flg = True
            
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
                            load, assign = None, []
                        else:
                            data[conv_num][param] = line.split(':=')[1].strip(',').strip().strip(',')
                else:
                    search_word = param
                    if search_word in line:
                        parameter = line.split(':=')[0].strip()
                        if ':= L' in line:
                            load = line.split(':=')[1].strip().strip('L').strip(' L,);').strip()
                            assign = data[conv_num]['load_identity'][load]
                            try:
                                data[conv_num][parameter] = assign.strip('"')
                            except:
                                data[conv_num][parameter] = assign
                            load, assign = None, []
                        elif ':=' in line:
                            try:
                                data[conv_num][parameter] = line.split(':=')[1].strip(',').strip().strip(',')
                            except Exception as e:
                                print(e)
    full_data[LAC_num] = data
    return full_data

def audit_file_ARSAW(f,keys,exact):
    """ Parse ARSAW .txt s7 file and extract desired features
    
        @param f: File currently being parsed
        @type f: File
        @param keys: ID list of parameters to parse from the file (add any number)
        @type keys: List[Str]
    """
    full_data = {}
    data = {}
    assign = []
    load = None
    long_assign = []
    long_assign_flg = False
    norm_assign_flg = False
    conv_num = None
    LAC_num = None
    parameters = generate_parameter_dict(keys)
    #TODO chekc if long and normal assign work together and check compatibility with ARSAW
    for line in f:
        if 'FUNCTION ' in line:
                data = {}
                LAC_num = line.split('"')[1]
                full_data[LAC_num] = data
        if 'TITLE' in line:
            if 'call FB SF' in line or 'call FB ACF' in line:
                conv_num = line.split('=')[1].strip()
                data[conv_num] = copy.deepcopy(parameters)
    
        if conv_num is not None:
            if ' A ' in line and not long_assign_flg:
                assign.append(line.strip().strip(';'))
                norm_assign_flg = True
            elif ' AN' in line and not long_assign_flg:
                assign.append(line.strip().strip(';'))
                norm_assign_flg = True
            elif ' O' in line and not long_assign_flg:
                assign.append(line.strip().strip(';'))
                norm_assign_flg = True
            elif ' ON' in line and not long_assign_flg:
                assign.append(line.strip().strip(';'))
                norm_assign_flg = True
            if ' = ' in line:
                load = line.split('=')[1].strip().strip('=L;').strip()
                if norm_assign_flg:
                    if long_assign != []:
                        assign.append(long_assign)
                        long_assign_flg = False
                        long_assign = []
                    data[conv_num]['load_identity'][load]=assign
                    assign = []
                    norm_assign_flg = False
                    load = False
                    
            if long_assign_flg:
                long_assign.append(line.strip().strip(';'))
                if ')' in line:
                    long_assign_flg = False

            if 'A(' in line:
                long_assign.append('A(')
                long_assign_flg = True
                norm_assign_flg = True

            if 'O(' in line:
                long_assign.append('O(')
                long_assign_flg = True
                norm_assign_flg = True
            
            if 'CALL' in line:
                data[conv_num]['Conveyor_model'] = line.split(',')[1].split('"')[1]
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
                            load, assign = None, []
                        else:
                            data[conv_num][param] = line.split(':=')[1].strip(',').strip().strip(',')
                else:
                    search_word = param
                    if search_word in line:
                        parameter = line.split(':=')[0].strip()
                        if ':= L' in line:
                            load = line.split(':=')[1].strip().strip('L').strip(' L,);').strip()
                            assign = data[conv_num]['load_identity'][load]
                            try:
                                data[conv_num][parameter] = assign.strip('"')
                            except:
                                data[conv_num][parameter] = assign
                            load, assign = None, []
                        elif ':=' in line:
                            try:
                                data[conv_num][parameter] = line.split(':=')[1].strip(',').strip().strip(',')
                            except:
                                pass
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
        @param save_name: Name to save the parsed .jso
        n file as
        @type save_name: Str
        @param exact: True if the exact keyword is to be searched, False if a line containing the word is to be searched
        @type exact: Bool
    """
    data = {}
    try:
        if 'ARSAW' in f:
            data = audit_file_ARSAW(open(f,'r'),keys, exact)
        else:
            data = audit_file_regular(open(f,'r'),keys, exact)
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

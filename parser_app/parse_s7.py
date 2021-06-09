import copy

import os
import json

def audit_file(f, keys):
    """Function to parse .txt file and extract desired features
    
    @param: f: file currently being parsed
    @param: keys: string ID list of parameters to parse from the file (add any number) """
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
                if ' ' + param +' ' in line:
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
    full_data[LAC_num] = data
    return full_data


def generate_parameter_dict(keys):
        """Function to generate dictionary storing and identifying parameters

        @param: keys: Desired parameters to extract """
        parameters = {'load_identity':{},'Conveyor_model':''}
        for key in keys:
                parameters[key]= ''
        return parameters

def begin_audit(f, keys,save_name):
    try:
        data = audit_file(open(f,'r'),keys)
    except Exception as e:
        print(f'File {f} was not found or does not exist')
        return
    key_string= ''
    for key in keys:
        key_string += str(key) +'-'
    sep = '/'
    folder_path =  sep.join(f.split('/')[:-1]).strip("[']")+'/'+str(key_string).strip('-')
    os.makedirs(folder_path,exist_ok=True)
    file_name = folder_path+'/'+save_name+'_parsed.json'
    with open(file_name,'w') as finish:
        finish.write(json.dumps(data, indent = 1))
    return file_name

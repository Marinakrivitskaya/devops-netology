# !/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import json
import yaml

#15_example.json
#15_example.yaml

if len (sys.argv) > 1:
    file_name=sys.argv[1]
else:
    raise BaseException ("Not enough arguments!")


def conv_json(file_name):
    try:
        with open (file_name, "r", encoding="utf-8") as fp:
            json_obj = json.load(fp)
            #print(json_obj)
    except json.JSONDecodeError as err:
        #print (f"ERROR: This file doesn't match the format json \n{err}")
        print(f"ERROR: This file doesn't match the format json or yaml.\n{err}")
        return 1
    try:
        #Проверяем корректность формата перед тем как записьть файл
        #yaml.dump(json_obj, sys.stdout)
        yaml.safe_dump(json_obj)
        #Получаем имя с новым расширением
        newfile_name=os.path.splitext(file_name)[0]+".yaml"
        with open (newfile_name, "w", encoding="utf-8") as fp:
            yaml.dump(json_obj, fp)
            return 0
    except yaml.YAMLError as err:
        print (f"ERROR Decode to yaml: \n{err}")


def conv_yaml(file_name):
    try:
        with open (file_name, "r", encoding="utf-8") as fp:
            yaml_obj = yaml.safe_load(fp)
            #print(yaml_obj)

    except yaml.YAMLError as err:
        #print (f"ERROR: This file doesn't match the format json \n{err}")
        print(f"ERROR: This file doesn't match the format yaml or json.\n{err}")
        return 1
    try:
       #Проверяем корректность формата перед тем как записьть файл
       json.dumps(yaml_obj)
       #Получаем имя с новым расширением
       newfile_name = os.path.splitext (file_name)[0] + ".json"
       with open (newfile_name, "w", encoding="utf-8") as fp:
            json.dump(yaml_obj, fp)
            return 0
    except json.JSONDecodeError as err:
        print (f"ERROR Decode to json: \n{err}")
        return 1

def pre_check(file_name):
    with open (file_name, "r", encoding="utf-8") as fp:
        for line in fp.readlines():
            if (line[0] == '-'):
                #print('YAML=', line[0])
                supposed_type = 'YAML'
            elif (line[0] == '{'):
                #print('JSON=', line[0])
                supposed_type = 'JSON'
            else:
                #fp.seek(0)
                supposed_type='YAML'
            break
    return supposed_type

supposed_type = pre_check(file_name)


if supposed_type == "JSON":
    return_conv = conv_json(file_name)
elif supposed_type == "YAML":
    return_conv = conv_yaml(file_name)
else:
    pass
# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

## Обязательные задания

1. Мы выгрузили JSON, который получили через API запрос к нашему сервису:

	```json
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
Нужно найти и исправить все ошибки, которые допускает наш сервис
     
```json
{
 "info" : "Sample JSON output from our service\\t",
  "elements" :[
    {
     "name" : "first",
     "type" : "server",
     "ip" : "71.75.22.43" 
    },
    {
     "name" : "second",
     "type" : "proxy",
     "ip" : "71.78.22.43"
    }
  ]
}
```

  
  

2. В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

```python
# !/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import json
import yaml
import time


site_list = ['drive.google.com', 'mail.google.com', 'google.com']
site_dict = {}

def check_list_of_sites(site_list, site_dict):

    for site_url in site_list:
        #print('site_url=', site_url )
        site_dict=check_site_dns(site_url, site_dict)
    return site_dict


def check_site_dns(site_url, site_dict):
    site_new_ip = []


    result_os = os.popen(f'dig +short {site_url} | grep  -E \'[0-9]\'')
    print('result_os=  ', result_os)

    for result in result_os:
        # For any ip delete \n
        site_new_ip.append(result.replace("\n",""))

        #print('site_new_ip= ', site_new_ip)

    print('site_new_ip: ', site_new_ip)

    if site_dict.get(site_url) != None:

        site_old_ip = site_dict[site_url]
        #print('site_old_ip: ', site_old_ip)
        i = 0
        #if true => need write to yaml\json files
        ip_changed = False
        while i < len(site_old_ip):
            if site_old_ip[i] == site_new_ip[i]:
                print(f'{site_url} - {site_old_ip[i]}.')
            else:
                print(f'[ERROR] {site_url} IP mismatch: {site_old_ip[i]} {site_new_ip[i]}.')                
                ip_changed = True
            i = i + 1

    else:
        #If it's first execution
        site_dict[site_url] = site_new_ip
        print('site_dict==', site_dict)
        ip_changed = True

    if ip_changed == True:
        with open("servers_ip.json", "w") as fp_json:
            json.dump(site_dict, fp_json)
        with open("servers_ip.yaml", "w") as fp_yaml:
            yaml.dump(site_dict, fp_yaml)

    return site_dict

while True:
    site_dict = check_list_of_sites(site_list, site_dict)
    print("site_dict==", site_dict)
    time.sleep(5)
```


## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

```python
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
```    

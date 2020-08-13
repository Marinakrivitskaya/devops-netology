# !/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import json
import yaml
import time

#dig +short google.com @8.8.8.8 | head -n 1

site_list = ['drive.google.com', 'mail.google.com', 'google.com']
site_dict = {}

def check_list_of_sites(site_list, site_dict):

    for site_url in site_list:
        #print('site_url=', site_url )
        site_dict=check_site_dns(site_url, site_dict)
    return site_dict


def check_site_dns(site_url, site_dict):
    #site_dict = site_dict
    #site_url = site_url
    site_new_ip = []


    #result_os = os.popen(f'dig +short {site_url} | grep  -E \'[0-9]\' | head -n 1 | tr -d \'\r\n\'')
    result_os = os.popen(f'dig +short {site_url} | grep  -E \'[0-9]\'')
    print('result_os=  ', result_os)

    for result in result_os:
        # For any ip delete \n
        site_new_ip.append(result.replace("\n",""))

        #print('site_new_ip= ', site_new_ip)

    print('site_new_ip: ', site_new_ip)

    if site_dict.get(site_url) != None:
        print('YES')
        #print(site_dict)
        #print('site_dict.get = ', site_dict.get(site_url))
        site_old_ip = site_dict[site_url]
        #print('site_old_ip: ', site_old_ip)
        i = 0
        ip_changed = False
        while i < len(site_old_ip):
            if site_old_ip[i] == site_new_ip[i]:
                #print('YES2')
                print(f'{site_url} - {site_old_ip[i]}.')
            else:
                print(f'[ERROR] {site_url} IP mismatch: {site_old_ip[i]} {site_new_ip[i]}.')
                ip_changed = True
            i = i + 1

            #json.yaml.dump(site_dict, )
    else:
        #If it's first execution
        #print('no')
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
    #site_dict = check_site_dns('google.com', site_dict)
    site_dict = check_list_of_sites(site_list, site_dict)
    print("site_dict==", site_dict)
    time.sleep(2)
else:
    print('Not Work')




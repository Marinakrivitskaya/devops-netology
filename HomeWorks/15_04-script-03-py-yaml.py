# !/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import sys
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

    result_os = os.popen(f'dig +short {site_url} | grep  -E \'[0-9]\' | head -n 1 | tr -d \'\r\n\'')
    for result in result_os:
        site_new_ip = result
        #print('site_new_ip: ', site_new_ip)
        #print('site_new_ip= ', site_new_ip)


    if site_dict.get(site_url) != None:
        #print('YES')
        #print(site_dict)
        #print('site_dict.get = ', site_dict.get(site_url))
        site_old_ip = site_dict[site_url]
        #print('site_old_ip: ', site_old_ip)

        if site_old_ip == site_new_ip:
            #print('YES2')
            print(f'{site_url} - {site_old_ip}.')
        else:
            print(f'[ERROR] {site_url} IP mismatch: {site_old_ip} {site_new_ip}.')
            site_dict[site_url] = site_new_ip
    else:
        #print('no')
        site_dict[site_url] = site_new_ip
        pass
    return site_dict

while True:
    #site_dict = check_site_dns('google.com', site_dict)
    site_dict = check_list_of_sites(site_list, site_dict)
    time.sleep(2)
else:
    print('Not Work')




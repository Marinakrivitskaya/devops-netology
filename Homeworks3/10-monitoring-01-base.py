# !/usr/bin/env python3
# -*- coding: utf8 -*-

__auth__ = 'Andrey Krylov'
__date__ = '26/01/2021'

import os
import sys
import subprocess
import json
import time
from datetime import datetime






def loadlavg():
    '''Read file: /proc/loadavg
    File /proc/loadavg Content: CPU LA in 1/5/15 min
    Out dict of:
        cpu_treads = amount of CPU treads
        cpu_la1 = CPU LA in 1 min
        cpu_la5 = CPU LA in 5 min
        cpu_la15 = CPU LA in 5 min
    '''
    try:
        loadlavg_dict = {}
        loadlavg_dict['cpu_treads'] = os.cpu_count()
        with open('/proc/loadavg', 'r') as loadavg_file:
            loadavg_line = loadavg_file.readline()
            loadavg_list = loadavg_line.split(' ')[:3]
            #print(loadavg_list)
            loadlavg_dict['cpu_la1'] = loadavg_list[0]
            loadlavg_dict['cpu_la5'] = loadavg_list[1]
            loadlavg_dict['cpu_la15'] = loadavg_list[2]
            return(loadlavg_dict)

    except IOError as e:
        print('ERROR: %s' % e)
        sys.exit(1)     # синоним raise SystemExit(3), 2-синтаксич;1-другие;0-успешено; <=255


#print(os.cpu_count())





def meminfo():
    '''Read file: /proc/meminfo
    File /proc/meminfo
    Out contents file /proc/meminfo as a dict
    '''
    try:
        file_path = '/proc/meminfo'
        meminfo_dict = {}
        with open(file_path, 'r') as meminfo_file:
            for meminfo_line in meminfo_file:
                meminfo_list = meminfo_line.split()[:2]
                meminfo_dict[meminfo_list[0]] = meminfo_list[1]
            return(meminfo_dict)
    except IOError as e:
        print('ERROR: %s' % e)
        sys.exit(1)





#Документация по статистики дисков
#https://www.kernel.org/doc/Documentation/block/stat.txt  - /sys/block/<dev>/stat file
def diskstats():
    '''Get info for disk using /proc/diskstats
    '''
    #https://www.kernel.org/doc/Documentation/iostats.txt  -  /proc/diskstats
    # columns_disk:
    # Field  1 -- # of reads completed
    # Field  2 -- # of reads merged, field 6 -- # of writes merged
    # Field  3 -- # of sectors read
    # Field  4 -- # of milliseconds spent reading
    # Field  5 -- # of writes completed
    # Field  6 -- # of writes merged
    # Field  7 -- # of sectors written
    # Field  8 -- # of milliseconds spent writing
    # Field  9 -- # of I/Os currently in progress
    # Field 10 -- # of milliseconds spent doing I/Os
    # Field 11 -- weighted # of milliseconds spent doing I/Os
    # Field 12 -- # of discards completed
    # Field 13 -- # of discards merged
    # Field 14 -- # of sectors discarded
    # Field 15 -- # of milliseconds spent discarding
    columns_disk = ['rd_comp', 'rd_mrg', 'rd_sector', 'ms_reading', 'wr_comp', 'wr_mrg', 'wr_sector',
                    'ms_writting', 'cur_ios', 'ms_doing_io', 'ms_weighted', 'disc_comp', 'disc_merg', 'disc_sect',
                    'ms_disc']

    # columns_part
    # Field  1 -- # of reads issued
    # Field  2 -- # of sectors read
    # Field  3 -- # of writes issued
    # Field  4 -- # of sectors written
    columns_part = ['rd_issued', 'rd_sector', 'wr_issued', 'wr_sector']

    try:
        len_columns_disk = len(columns_disk)
        len_columns_part = len(columns_part)
        file_path = '/proc/diskstats'
        diskstats_dict = {}
        with open(file_path, 'r') as diskstats_file:
            for diskstats_line in diskstats_file:
                lines_dict = {}
                #print(diskstats_line)
                diskstats_name = diskstats_line.split()[2]
                diskstats_line = diskstats_line.split()[3:]
                #print(diskstats_name)
                #print(diskstats_line)
                if len(diskstats_line) == len_columns_disk:
                    for metric_name, metric_value in zip(columns_disk, diskstats_line):
                        lines_dict[metric_name] = metric_value
                elif len(diskstats_line) == len_columns_part:
                    for metric_name, metric_value in zip(columns_part, diskstats_line):
                        lines_dict[metric_name] = metric_value


                ####################
                #Data from df -i
                df_output = subprocess.run(["df", "-i", f"/dev/{diskstats_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                df_date = df_output.stdout.decode().split()[8:]
                lines_dict["Inodes"] = df_date[0]
                lines_dict["IUsed"] = df_date[1]
                lines_dict["IFree"] = df_date[2]
                lines_dict["IUsed%"] = df_date[3]

                diskstats_dict[diskstats_name] = lines_dict
            return(diskstats_dict)
    except IOError as e:
        print('ERROR: %s' % e)
        sys.exit(1)





def netdev():
    '''Get info for disk using /proc/net/dev
    '''
    columns_net = ['rv_bytes', 'rv_packets', 'rv_errs', 'rv_drop', 'rv_fifo', 'rv_frame',
                    'rv_comp', 'rv_mult', 'tran_bytes', 'tran_packets', 'tran_errs', 'tran_drop', 'tran_fifo',
                   'tran_colls', 'rv_carr', 'rv_comp']

    try:
        file_path = '/proc/net/dev'
        netdev_dict = {}
        with open(file_path, 'r') as netdev_file:
            #Пропустить первые 2 строки c заголовком
            netdev_file.readline()
            netdev_file.readline()
            for netdev_line in netdev_file:
                lines_dict = {}
                line_list = netdev_line.split()
                interface = line_list[0]
                interface_data = line_list[1:]
                #print(interface_data)
                for metric_name, metric_value in zip(columns_net, interface_data):
                    lines_dict[metric_name] = metric_value
                netdev_dict[interface] = lines_dict

            return(netdev_dict)
    except IOError as e:
        print('ERROR: %s' % e)
        sys.exit(1)

def main():
    result_dict = {}
    # файл    в  директорию /var/log/'YY-MM-DD-awesome-monitoring.log'
    date_of_file = datetime.today().strftime('%y-%m-%d')
    print(date_of_file)
    file_name = f'/var/log/{date_of_file}-awesome-monitoring.log'
    #file_name = f'/tmp/{date_of_file}-awesome-monitoring.log'
    # print(meminfo())
    # print(diskstats())
    # print(netdev())
    # print(loadlavg())
    # 1)timestamp (временная метка, int, unixtimestamp)
    timestamp = int(time.time())
    # print(f'Time: {timestamp}')

    result_dict ['timestamp'] = timestamp
    result_dict['loadlavg'] = loadlavg()
    result_dict['meminfo'] = meminfo()
    result_dict['diskstats'] = diskstats()
    result_dict['netdev'] = netdev()

    try:
        with open(file_name, 'ab') as fp:
            fp.write(json.dumps(result_dict).encode("utf-8"))
            fp.write(('\n').encode("utf-8")) #перенос строки
    except json.JSONEncoder as err:
        return 1
    except IOError as e:
        print('ERROR: %s' % e)
        sys.exit(1)

    return result_dict



if __name__ == '__main__':
    main()


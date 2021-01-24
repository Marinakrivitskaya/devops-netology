# !/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import json
import yaml



#1)timestamp (временная метка, int, unixtimestamp)
import time
timestamp = int(time.time())
print(f'test {timestamp}')

stat1 = open('/proc/stat', 'r')
lst1 = stat1.readlines()
print(lst1)
idle1 = int(lst1[0].split(' ')[5])
print(idle1)
print('___________________')
#/proc/stat — для информации о процессоре.
# Данные тут отображают количество времени, которое CPU тратит на выполнение различных задач. Эти данные (time units) предоставлены как USER_HZ — сотые доли секунды.
# Значение колонок по очереди:
# — user: обычные процессы, которые выполняются в user mode;
# — nice: процессы с nice в user mode;
# — system: процессы в kernel mode;
# — idle: время в простое;
# — iowait: ожидание операций I/O;
# — irq: обработка прерываний;
# — softirq: обработка  softirqs;
# — steal: «украденное» время, потраченное другими операционными системами при использовании виртуализации; (см. тут>>> и тут>>>)
# — guest: обработка «гостевых» (виртуальных) процессоров;


def cput():
    ''' Reads /proc/stat file, if extis.
       Get amount of:
                   'user'
                   'nice'
                   'system'
                   'idle'
                   'iowait'
                   'irq'
                   'softirq'
                   'steal'
                   'steal'.

        Returns sum of total used times by CPU.'''

    try:
        with open('/proc/stat', 'r') as procfile:
            cputimes = procfile.readline()
            cputotal = 0
            for i in cputimes.split(' ')[2:]:
                i = int(i)
                cputotal = (cputotal + i)
            return (float(cputotal))
    except IOError as e:
        print('ERROR: %s' % e)
        sys.exit(3)

#print(cput())



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
            print(loadavg_list)
            loadlavg_dict['cpu_la1'] = loadavg_list[0]
            loadlavg_dict['cpu_la5'] = loadavg_list[1]
            loadlavg_dict['cpu_la15'] = loadavg_list[2]
            return(loadlavg_dict)

    except IOError as e:
        print('ERROR: %s' % e)
        sys.exit(1)     # синоним raise SystemExit(3), 2-синтаксич;1-другие;0-успешено; <=255


print(os.cpu_count())
print(loadlavg())
print('___________________')




def meminfo():
    '''Read file: /proc/meminfo
    File /proc/meminfo
    Out contents file /proc/meminfo as a dict
    '''
    try:
        meminfo_dict = {}
        with open('/proc/meminfo', 'r') as meminfo_file:
            for meminfo_line in meminfo_file:
                meminfo_list = meminfo_line.split()[:2]
                meminfo_dict[meminfo_list[0]] = meminfo_list[1]
            return(meminfo_dict)
    except IOError as e:
        print('ERROR: %s' % e)
        sys.exit(1)

print(meminfo())
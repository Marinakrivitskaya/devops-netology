# -*- coding: utf8 -*-


boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

boys = sorted (boys)
girls = sorted (girls)

if len (boys) == len (girls):
    i = 0
    dlina = len (boys)
    while i < dlina:
        print (f'{boys[i]} и {girls[i]}')
        i += 1
else:
    print ('Внимание, кто-то может остаться без пары!')

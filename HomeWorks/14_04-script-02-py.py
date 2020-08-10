# -*- coding: cp1251 -*-
# !/usr/bin/env python3
import os

bash_command = ["cd C:\\Users\\kaa\\PycharmProjects\\DevOps\\devops-netology\\HomeWorks", "git status"]
result_os = os.popen (' && '.join(bash_command)).read ()
is_change = False
for result in result_os.split ('\n'):
    if result.find ('modified') != -1:
        prepare_result = result.replace ('\tmodified:   ', '')
        print (prepare_result)
        break


# Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать какие файлы модифицированы в
#репозитории, относительно локальных изменений. Этим скриптом недовольно начальство,
#потому что в его выводе не хватает изменённых файлов
#и не понятно, в какой директории они находятся.
#  Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?
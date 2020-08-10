# !/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import sys

#check_dir='~/Git_test/testhook/f1/'
check_dir=sys.argv[1]

def git_status(check_dir):
    check_dir=os.path.expanduser(check_dir)
    #git_dir=os.path.expanduser('~/Git_test/testhook/')

    bash_command = [f'cd {check_dir}', f'git status {check_dir}']
    print(bash_command)
    result_os = os.popen (' && '.join(bash_command)).read ()
    print(result_os)
    is_change = False
    for result in result_os.split ('\n'):
        if result.find ('modified') != -1:
            prepare_result = result.replace ('\tmodified:   ', '')
            print(os.path.join(check_dir,prepare_result))
            #break
    return 0

git_status(check_dir)

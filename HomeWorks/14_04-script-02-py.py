# !/usr/bin/env python3
# -*- coding: utf8 -*-
import os

git_dir=os.path.expanduser('~/Git_test/testhook')

bash_command = [f'cd {git_dir}', 'git status']
print(bash_command)
result_os = os.popen (' && '.join(bash_command)).read ()
print(result_os)
is_change = False
for result in result_os.split ('\n'):
    if result.find ('modified') != -1:
        prepare_result = result.replace ('\tmodified:   ', '')
        print(os.path.join(git_dir,prepare_result))
        #break


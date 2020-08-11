# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательные задания

>1. Есть скрипт:  
	```python    
    #!/usr/bin/env python3    
	a = 1  
	b = '2'  
	c = a + b  
	```  
	 
>* Какое значение будет присвоено переменной c?  
	
Будет ошибка о том, что операнд не применим к данным типам  
	
>* Как получить для переменной c значение 12?

    ```python
	a = '1'  
    b = '2'  
    c = a + b  
    print(c)  
    ```
	
>* Как получить для переменной c значение 3?
	
    ```python  	
	a = 1  
    b = 2  
    c = a + b  
    print(c)  
    ```   
	

>2. Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе не хватает изменённых файлов и не понятно, в какой директории они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

	```python
    #!/usr/bin/env python3

    import os

	bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
	result_os = os.popen(' && '.join(bash_command)).read()
    is_change = False
	for result in result_os.split('\n'):
        if result.find('modified') != -1:
            prepare_result = result.replace('\tmodified:   ', '')
            print(prepare_result)
            break

	```

```python
# !/usr/bin/env python3
# -*- coding: utf8 -*- 
import os   
   
git_dir=os.path.expanduser('~/netology/sysadm-homeworks')   
   
bash_command = [f'cd {git_dir}', 'git status']   
   
result_os = os.popen (' && '.join(bash_command)).read ()   
   
is_change = False  
for result in result_os.split ('\n'):  
    if result.find ('modified') != -1:  
        prepare_result = result.replace ('\tmodified:   ', '')  
        print(os.path.join(git_dir,prepare_result))  
        #break  
```


>3. Доработать скрипт выше так, чтобы он мог проверять локальный репозиторий в директории, которую мы передаём, как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.
 
 ```python 
# !/usr/bin/env python3  
# -*- coding: utf8 -*-  
import os  
import sys  

check_dir=sys.argv[1]

def git_status(check_dir):
    check_dir=os.path.expanduser(check_dir)
    bash_command = [f'cd {check_dir}', f'git status {check_dir}']

    result_os = os.popen (' && '.join(bash_command)).read ()

    is_change = False
    for result in result_os.split ('\n'):
        if result.find ('modified') != -1:
            prepare_result = result.replace ('\tmodified:   ', '')
            print(os.path.join(check_dir,prepare_result))
            #break
    return 0

git_status(check_dir)
```

>4. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.

 ```python 
# !/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import sys
import time

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
	
    #grep сделал, так как CNAME выдают некоторые сайты, head – так как по факту имеют несколько ip
    result_os = os.popen(f'dig +short {site_url} | grep  -E \'[0-9]\' | head -n 1 | tr -d \'\r\n\'')
    for result in result_os:
        site_new_ip = result
        #print('site_new_ip= ', site_new_ip)


    if site_dict.get(site_url) != None:
        #print('site_dict.get = ', site_dict.get(site_url))
        site_old_ip = site_dict[site_url]
        #print('site_old_ip: ', site_old_ip)

        if site_old_ip == site_new_ip:
            print(f'{site_url} - {site_old_ip}.')
        else:
            print(f'[ERROR] {site_url} IP mismatch: {site_old_ip} {site_new_ip}.')
            site_dict[site_url] = site_new_ip
    else:
        site_dict[site_url] = site_new_ip
        pass
    return site_dict

while True:
    #site_dict = check_site_dns('google.com', site_dict)
    site_dict = check_list_of_sites(site_list, site_dict)
    time.sleep(5)
```

>Дополнительное задание (со звездочкой*) - необязательно к выполнению  
>Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, то нам приходится каждый раз переносить архив с нашими изменениями с сервера на наш локальный компьютер, формировать новую ветку, коммитить в неё изменения, создавать pull request (PR) и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. Мы хотим максимально автоматизировать всю цепочку действий. Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым). При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений кофнигурации. С директорией локального репозитория можно делать всё, что угодно. Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, так и при слиянии в master. Важно получить конечный результат с созданным PR, в котором применяются наши изменения.   

 ```python 
# !/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import sys


from github import Github
#https://github.com/PyGithub/PyGithub
#https://developer.github.com/v3/repos/
#https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
#https://pygithub.readthedocs.io/en/latest/examples.html

if len (sys.argv) > 1:
    pr_body=sys.argv[1]
    print("pr_body= ",pr_body)
else:
    raise BaseException ("Not enough arguments!")


#Переходим в каталог репозитория
os.popen('cd /home/kaa/PycharmProjects/DevOps/devops-netology/')
print(os.getcwd())

#Создаем ветку
print(os.popen("git checkout -b conf-merge"))
#print(os.popen("git checkout  conf-merge"))

#Коммит изменений
print(os.popen("git commit -a -m 'new_config'"))

#Отправьте новую ветку в репозиторий на гитхабе
print(os.popen("git push -u origin conf-merge"))

#Подключаемся используя Токен
g = Github("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
g = Github(base_url="https://api.github.com", login_or_token="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

#Просматриваем все репозитории
for repo in g.get_user().get_repos():
    print(repo.name)

#Выбираем репозиторий
repo = g.get_user().get_repo("devops-netology")
print(repo)

#Делаем Pull Request
pr = repo.create_pull(title="Request for merge conf-merge with master", body=pr_body, head="conf-merge", base="master")
```
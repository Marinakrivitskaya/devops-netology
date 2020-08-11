# -*- coding: utf8 -*-
import os
import sys

#https://github.com/PyGithub/PyGithub
from github import Github
#https://developer.github.com/v3/repos/
#https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
#https://pygithub.readthedocs.io/en/latest/examples/PullRequest.html
#https://pygithub.readthedocs.io/en/latest/examples.html


if len (sys.argv) > 1:
    pr_body=sys.argv[1]
    print("pr_body= ",pr_body)
else:
    raise BaseException ("Not enough arguments!")

#Переходим в каталог репозитория
os.popen("cd C:\\Users\\kaa\\PycharmProjects\\DevOps\\devops-netology\\HomeWorks")
print(os.getcwd())
#print(os.popen("git branch conf-merge"))
#print(os.popen("git checkout  conf-merge"))
print(os.popen("git checkout -b conf-merge"))


#Подключаемся используя Токен
g = Github("7523e782b42ba44b11a6ab1eb7ca364c576cdd0a")
g = Github(base_url="https://api.github.com", login_or_token="4cdd014c69f4c00aeb36e5eea002eb5e02950ac3")


# Then play with your Github objects:

#Просматриваем все репозитории
for repo in g.get_user().get_repos():
    print(repo.name)

#Выбираем репозиторий
repo = g.get_user().get_repo("devops-netology")
print(repo)

# Тело для Pull Request
body = '''
SUMMARY
Change HTTP library used to send requests

TESTS
  - [x] Send 'GET' request
  - [x] Send 'POST' request with/without body
'''

#Делаем Pull Request
#pr = repo.create_pull(title="Use 'requests' instead of 'httplib'", body=body, head="fix", base="master")



#Просмотреть список
#print(list(repo.get_branches()))

#Create a new Pull Request
#>>> repo = g.get_repo("PyGithub/PyGithub")
#>>> body = '''
#>>> SUMMARY
#>>> Change HTTP library used to send requests
#>>>
#>>> TESTS
#>>>   - [x] Send 'GET' request
#>>>   - [x] Send 'POST' request with/without body
#>>> '''
#>>> pr = repo.create_pull(title="Use 'requests' instead of 'httplib'", body=body, head="develop", base="master")
#>>> pr



##Get Pull Requests by Query
#pulls = repo.get_pulls(state='open', sort='created', base='master')
#for pr in pulls:
#    print(pr.number)

#Вам необходимо передать следующие аргументы:
#path - string - путь к контенту.
#ref - string - имя тега commit/branch/tag. По умолчанию: ветвь по умолчанию репозитория (обычно мастер)
#Например - repo.get_contents('config/version.rb','development')

#contents = repo.get_contents('.gitignore','master')
#print(contents)


#Как следует из документации, вызов create_file объекта github.Repository
# Repository должен создать файл, но я получаю github.GithubException.UnknownObjectException.
#repo.create_file('/filename', 'commitmessage', 'content')
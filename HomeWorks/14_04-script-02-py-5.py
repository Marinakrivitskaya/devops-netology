# -*- coding: utf8 -*-
import os
import sys
import time

#https://github.com/PyGithub/PyGithub
from github import Github
#https://developer.github.com/v3/repos/
#https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
#https://pygithub.readthedocs.io/en/latest/examples/PullRequest.html
#https://pygithub.readthedocs.io/en/latest/examples.html

g = Github("7523e782b42ba44b11a6ab1eb7ca364c576cdd0a")
g = Github(base_url="https://api.github.com", login_or_token="7523e782b42ba44b11a6ab1eb7ca364c576cdd0a")

# Then play with your Github objects:


for repo in g.get_user().get_repos():
    print(repo.name)

repo = g.get_user().get_repo("devops-netology")
print(repo)




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
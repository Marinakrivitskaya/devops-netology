# Домашнее задание к занятию "5.4. Практические навыки работы с Docker"



> **Задача 1**
>
> В данном задании вы научитесь изменять существующие Dockerfile, адаптируя их под нужный инфраструктурный стек.
>
>  
>
> Измените базовый образ предложенного Dockerfile на Arch Linux c сохранением его функциональности.
>
>  
>
> \```text
>
> FROM ubuntu:latest
>
>  
>
> RUN apt-get update && \
>
>   apt-get install -y software-properties-common && \
>
>   add-apt-repository ppa:vincent-c/ponysay && \
>
>   apt-get update
>
>  
>
> RUN apt-get install -y ponysay
>
>  
>
> ENTRYPOINT ["/usr/bin/ponysay"]
>
> CMD ["Hey, netology”]
>
> \```
>
>  
>
> Для получения зачета, вам необходимо предоставить:
>
> \- Написанный вами Dockerfile
>
> \- Скриншот вывода командной строки после запуска контейнера из вашего базового образа
>
> \- Ссылку на образ в вашем хранилище docker-hub



**#docker pull archlinux** 

**Dockerfile:**

*FROM archlinux:latest*

 

*RUN pacman -Sy* *&& \*

*pacman -S --noconfirm community/ponysay*

 

*ENTRYPOINT ["/usr/bin/ponysay"]*

*CMD ["Hey, netology”]



**#docker build -t kaaa/archlinux:ponysay .**



**#docker run kaaa/archlinux:ponysay "Hi again"**

http://prntscr.com/ux9fyy



**Ссылка на образ в хранилище docker-hub:**

**https://hub.docker.com/r/kaaa/archlinux/tags**







> **Задача 2**
>
> В данной задаче вы составите несколько разных Dockerfile для проекта Jenkins, опубликуем образ в `dockerhub.io` и посмотрим логи этих контейнеров.
>
> \- Составьте 2 Dockerfile:
>
>   \- Общие моменты:
>
> ​    \- Образ должен запускать [Jenkins server](https://www.jenkins.io/download/)   
>
>   **- Спецификация первого образа:**
>
> ​    \- Базовый образ - [amazoncorreto](https://hub.docker.com/_/amazoncorretto)
>
> ​    \- Присвоить образу тэг `ver1` 
>
>   **- Спецификация второго образа:**
>
> ​    \- Базовый образ - [ubuntu:latest](https://hub.docker.com/_/ubuntu)
>
> ​    \- Присвоить образу тэг `ver2` 
>
> \- Соберите 2 образа по полученным Dockerfile
>
> \- Запустите и проверьте их работоспособность
>
> \- Опубликуйте образы в своём dockerhub.io хранилище
>
> Для получения зачета, вам необходимо предоставить:
>
> \- Наполнения 2х Dockerfile из задания
>
> \- Скриншоты логов запущенных вами контейнеров (из командной строки)
>
> \- Скриншоты веб-интерфейса Jenkins запущенных вами контейнеров (достаточно 1 скриншота на контейнер)
>
> \- Ссылки на образы в вашем хранилище docker-hub



### Создание контейнера Jenkins в amazoncorreto

**#docker pull amazoncorretto**



**Dockerfile:**

*FROM amazoncorretto*

 

*LABEL Andrey K. kaa.a.a@mail.ru*

 

*#Установка репозитория Jenkins*

*RUN yum install -y wget*

*RUN wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo*

*RUN rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key*

 

*# запуск Jenkins*

*RUN yum install -y jenkins*

*#в пакет входить утилита ss*

*RUN yum install -y iproute*

 

*#Порт для Jenkins*

*EXPOSE 8080*

 

*#java -jar /usr/lib/jenkins/jenkins.war*

*CMD ["java", "-jar", "/usr/lib/jenkins/jenkins.war"]*

\##или можно было так:

\#ENTRYPOINT ["java"]

\#CMD ["-jar", "/usr/lib/jenkins/jenkins.war"]





Сборка образа

**#docker build -t amazoncorretto:ver1 .**

Запуск контейнера

**#docker run -p 8080:8080 -ti amazoncorretto:ver1**

http://prntscr.com/ux9gza

http://prntscr.com/ux9h2n



**\#docker exec d46ab1d9bf32 cat /root/.jenkins/secrets/initialAdminPassword**

*388694d42064442aa12d1e007c2138e1*

И т.д….



###  **Создание контейнера** **Jenkins в** **Ubuntu**

**\#docker pull ubuntu:latest**

 

**Dockerfile:**

*FROM ubuntu:latest*

 

*LABEL Andrey K. kaa.a.a@mail.ru*

 

*#Установка репозитория Jenkins*

*RUN apt-get update -y*

 

*RUN apt-get install -y wget*

*RUN apt-get install -y gnupg && \*

*wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | apt-key add – && \*

*echo deb https://pkg.jenkins.io/debian-stable binary/ >> /etc/apt/sources.list*

 

*RUN apt-get update -y*

*RUN apt-get install -y Jenkins*

 

*#для утилиты* *ss*

*RUN apt-get install -y iproute2*

 

*#Java в* *тихом* *режиме*

*RUN apt-get install -y openjdk-8-jdk-headless*

 

*#Порт для Jenkins*

*EXPOSE 8080*

 

*#java -jar /usr/lib/jenkins/jenkins.war*

*CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war"]*



Сборка образа

**#docker build -t ubuntu:ver2 .**

Запуск контейнера, проброс порта на 8081 хоста

**#docker run -p 8081:8080 -ti ubuntu:ver2**

http://prntscr.com/ux9ic1

http://prntscr.com/ux9ipn



Добавляем в тег имя пользователя: 

**#docker tag amazoncorretto:ver1 kaaa/amazoncorretto:ver1**

**#docker tag ubuntu:ver2 kaaa/ubuntu:ver2**

 

Загружаем образы в dockerhub

**#docker push kaaa/amazoncorretto:ver1**

**\#docker push kaaa/ubuntu:ver2**

 

 

Ссылки на образы в хранилище docker-hub:

https://hub.docker.com/r/kaaa/amazoncorretto/tags

https://hub.docker.com/r/kaaa/ubuntu/tags/









> **Задача 3**
>
> В данном задании вы научитесь:
>
> - объединять контейнеры в единую     сеть
> - исполнять команды     "изнутри" контейнера
>
> Для выполнения задания вам нужно:
>
> ·     Написать Dockerfile:
>
> - - Использовать образ https://hub.docker.com/_/node как      базовый
>   - Установить необходимые зависимые      библиотеки для запуска npm приложения https://github.com/simplicitesoftware/nodejs-demo
>   - Выставить у приложения (и      контейнера) порт 3000 для прослушки входящих запросов
>   - Соберите образ и запустите контейнер      в фоновом режиме с публикацией порта
>
> ·     Запустить второй контейнер из образа ubuntu:latest
>
> ·     Создайть `docker network` и добавьте в нее оба запущенных контейнера
>
> ·     Используя `docker exec` запустить командную строку контейнера `ubuntu` в интерактивном режиме
>
> ·     Используя утилиту `curl` вызвать путь `/` контейнера с npm приложением
>
> Для получения зачета, вам необходимо предоставить:
>
> - Наполнение Dockerfile с npm     приложением
> - Скриншот вывода вызова команды     списка docker сетей (docker network cli)
> - Скриншот вызова утилиты curl с успешным     ответом



### Подготовка образа Node

**#docker pull** **node:latest**





**Dockerfile:**

*FROM node:latest*

 

*LABEL Andrey K. kaa.a.a@mail.ru*

 

*#Обновляем npm*

*RUN npm install npm@latest -g*

*RUN npm update*

 

*#Рабочая директория*

*WORKDIR /root*

 

*#Скачиваем архив с java-приложением*

*#Распаковываем архив с java-приложением*

*RUN wget https://github.com/simplicitesoftware/nodejs-demo/archive/master.zip && \*

*unzip master.zip && \*

*rm -f master.zip*

 

 

*#Переходим в директорию с программой*

*WORKDIR /root/nodejs-demo-master/*

 

*#устанавливаем* *java-приложение*

*RUN* *npm* *install*

 

*#Порт для* *nodejs*

*EXPOSE 3000*

 

*#запускаем* *java-приложение*

*#npm start*

*CMD ["npm", "start","node1"]*

 

 

 Собираем образ
**docker build -t node:demo1 .**





По дефолту создается bridge, но мы все же укажем

**#docker network create --subnet 192.168.90.0/24 --gateway=192.168.90.1 --ip-range 192.168.90.0/24 node-network**

*9179393857f5b060459a3f62792c5e622986c76bb9767e49be42f8450d9583fa*



Запуск контейнера с Node

**docker run -p 3000:3000 -dt --name=node1 --net=node-network node:demo1**



**# docker exec node1 ip a**

***…192.168.90.2..\***



Запуск контейнера с Ubuntu

**#docker run -dt --name=node2 --net=node-network ubuntu:latest**

**#docker exec node2 apt-get update**

**#docker exec node2 apt-get install -y curl**

**#docker exec -ti node2 /bin/bash**



Вызов curl / контейнера с npm приложением, node1 – имя машины с npm-приложением

**root@eb5585a32398#curl node1:3000/**

**>Скриншот вызова утилиты** **curl с успешным ответом**

http://prntscr.com/ux96vv







Список сетей

**# docker network ls**

*NETWORK ID     NAME        DRIVER       SCOPE*

*a2fcc636ed44    bridge       bridge       local*

*845aea18621c    host        host        local*

*9179393857f5    node-network    bridge       local*

*c24980c4667e    none        null        local*

 

**# docker network inspect node-network**

*[*

  *{*

​    *"Name": "node-network",*

​    *"Id": "9179393857f5b060459a3f62792c5e622986c76bb9767e49be42f8450d9583fa",*

​    *"Created": "2020-10-10T00:16:37.298461259+03:00",*

​    *"Scope": "local",*

​    *"Driver": "bridge",*

​    *"EnableIPv6": false,*

​    *"IPAM": {*

​      *"Driver": "default",*

​      *"Options": {},*

​      *"Config": [*

​        *{*

​          *"Subnet": "192.168.90.0/24",*

​          *"IPRange": "192.168.90.0/24",*

​          *"Gateway": "192.168.90.1"*

​        *}*

​      *]*

​    *},*

​    *"Internal": false,*

​    *"Attachable": false,*

​    *"Ingress": false,*

​    *"ConfigFrom": {*

​      *"Network": ""*

​    *},*

​    *"ConfigOnly": false,*

​    *"Containers": {*

​      *"e21e68571c3a489d62b6dc2ff8346a822a473d6f4c88553edd011d53e8fe0359": {*

​        *"Name": "node1",*

​        *"EndpointID": "e570acc7828b7f62b67ef2546f33a72834848e27eacfcbba8e4c6286bfea4e02",*

​        *"MacAddress": "02:42:c0:a8:5a:02",*

​        *"IPv4Address": "192.168.90.2/24",*

​        *"IPv6Address": ""*

​      *},*

​      *"eb5585a3239858500af635fcf1651d4dcad97b6b168eca5188f1b482736b0d7e": {*

​        *"Name": "node2",*

​        *"EndpointID": "65e51fc47c8da05534aea72a08a8a0a0a0506c7c75994a39f52081b89bda3b7a",*

​        *"MacAddress": "02:42:c0:a8:5a:03",*

​        *"IPv4Address": "192.168.90.3/24",*

​        *"IPv6Address": ""*

​      *}*

​    *},*

​    *"Options": {},*

​    *"Labels": {}*

  *}*

*]*

 

**>Скриншот вывода вызова команды списка** **docker сетей (****docker** **network** **cli)**

http://prntscr.com/ux980y




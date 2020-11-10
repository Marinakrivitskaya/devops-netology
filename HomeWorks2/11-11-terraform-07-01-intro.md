> # Домашнее задание к занятию "7.1. Инфраструктура как код"
>
> ## Задача 1. Выбор инструментов.
>
> ### Легенда
>
> Через час совещание на котором менеджер расскажет о новом проекте. Начать работу над которым надо будет уже сегодня. На данный момент известно, что это будет сервис, который ваша компания будет предоставлять внешним заказчикам. Первое время, скорее всего, будет один внешних клиент, со временем внешних клиентов станет больше.
>
> Так же по разговорам в компании есть вероятность, что техническое задание еще не четкое, что приведет к большому количеству небольших релизов, тестирований интеграций, откатов, доработок, то есть скучно не будет.
>
> Вам, как девопс инженеру, будет необходимо принять решение об инструментах для организации инфраструктуры. На данный момент в вашей компании уже используются следующие инструменты:
>
> - остатки Сloud Formation,
> - некоторые образы сделаны при помощи Packer,
> - год назад начали активно использовать Terraform,
> - разработчики привыкли использовать Docker,
> - уже есть большая база Kubernetes конфигураций,
> - для автоматизации процессов используется Teamcity,
> - также есть совсем немного Ansible скриптов,
> - и ряд bash скриптов для упрощения рутинных задач.
>
> Для этого в рамках совещания надо будет выяснить подробности о проекте, что бы в итоге определиться с инструментами:
>
> 1. Какой тип инфраструктуры будем использовать для этого проекта: изменяемый или не изменяемый?
> 2. Будет ли центральный сервер для управления инфраструктурой?
> 3. Будут ли агенты на серверах?
> 4. Будут ли использованы средства для управления конфигурацией или инициализации ресурсов?
>
> В связи с тем, что проект стартует уже сегодня, в рамках совещания надо будет определиться со всеми этими вопросами.
>
> ### В результате задачи необходимо
>
> 1. Ответить на четыре вопроса представленных в разделе "Легенда".
> 2. Какие инструменты из уже используемых вы хотели бы использовать для нового проекта?
> 3. Хотите ли рассмотреть возможность внедрения новых инструментов для этого проекта?
>
> Если для ответа на эти вопросы недостаточно информации, то напишите какие моменты уточните на совещании.



>  1.Ответить на четыре вопроса представленных в разделе "Легенда".



1) Сразу с самого начала я бы выбрал неизменяемую инфраструктуру. Что позволит в дальнейшем более просто продублировать инфраструктуру для новых заказчиков. А также позволит легче на этапе разработки откатываться к предыдущим состояниям, что потребуется по условиям задания. 

2) Без наличия центрального сервера для управления инфраструктурой. Данный выбор сделан исходя из расчета того, что будет использоваться Terraform (у него по умолчанию нет центрального хранилища).

3) Без наличия дополнительных агентов. (исходя из выбора планируемых инструментов)

4) Для инициализации использовать Terraform. 

 

> 2.Какие инструменты из уже используемых вы хотели бы использовать для нового проекта?



1) Инициализация - Terraform - создаем серверы, сеть, балансировка.    

2) Packer образы - используем образы вирт. машин, которые содержат в себе Kubbernetes.     

Тоесть создали оркестрацию.       

3)  При помощи оркестрации Kubbernetes будут разворачиваться контейнеры на виртуальных машинах.        

  Для предварительного тестирования на своих машинах разработчики могут использовать Docker, к чему они привыкли.        
  

>3.Хотите ли рассмотреть возможность внедрения новых инструментов для этого проекта?         

Думаю, что нет, приведенный список инструментов, которые использовались в организации являются майнстримом и дают разнообразный выбор в        зависимости от вариантов их сочетания.        

 

> Если для ответа на эти вопросы недостаточно информации, то напишите какие моменты уточните на совещании.         



Что я до конца не понял, и уточнил бы. У данного сервиса будет одна точка входа для всех клиентов. Или для каждого нового клиента будет изолированный сервис. Будет ли использоваться СУБД и если да, то какую выбрали разработчики. 



> ## Задача 2. Установка терраформ.
>
> Официальный сайт: https://www.terraform.io/
>
> Установите терраформ при помощи менеджера пакетов используемого в вашей операционной системе. В виде результата этой задачи приложите вывод команды `terraform --version`.



**#apt install terraform**

 

**#terraform --version**



*Terraform v0.13.5*





> ## Задача 3. Поддержка легаси кода.
>
> В какой-то момент вы обновили терраформ до новой версии, например с 0.12 до 0.13. А код одного из проектов на столько устарел, что не может работать с версией 0.13. В связи с этим необходимо сделать так, чтобы вы могли одновременно использовать последнюю версию терраформа установленную при помощи штатного менеджера пакетов и устаревшую версию 0.12.
>
> В виде результата этой задачи приложите вывод `--version` двух версий терраформа доступных на вашем компьютере или виртуальной машине.



**#cd /tmp/**

**#wget https://releunxipases.hashicorp.com/terraform/0.12.29/terraform_0.12.29_linux_amd64.zip**

**#unzip terraform_0.12.29_linux_amd64.zip**

**#whereis terraform**

**#cp terraform /usr/bin/terraform12**

 

**\#terraform12 –version**

*Terraform v0.12.29*

*Your version of Terraform is out of date! The latest version*

*is 0.13.5. You can update by downloading from* [*https://www.terraform.io/downloads.html*](https://www.terraform.io/downloads.html)

 

**#terraform --version**

*Terraform v0.13.5*













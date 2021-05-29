# Домашнее задание к занятию "12.1 Компоненты Kubernetes"

Вы DevOps инженер в крупной компании с большим парком сервисов. Ваша задача — разворачивать эти продукты в корпоративном кластере. 

## Задача 1: Установить Minikube

> Для экспериментов и валидации ваших решений вам нужно подготовить тестовую среду для работы с Kubernetes. Оптимальное решение — развернуть на рабочей машине Minikube.
>
> ### Как поставить на AWS:
> - создать EC2 виртуальную машину (Ubuntu Server 20.04 LTS (HVM), SSD Volume Type) с типом **t3.small**. Для работы потребуется настроить Security Group для доступа по ssh. Не забудьте указать keypair, он потребуется для подключения.
> - подключитесь к серверу по ssh (ssh ubuntu@<ipv4_public_ip> -i <keypair>.pem)
> - установите миникуб и докер следующими командами:
>   - curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
>   - chmod +x ./kubectl
>   - sudo mv ./kubectl /usr/local/bin/kubectl
>   - sudo apt-get update && sudo apt-get install docker.io conntrack -y
>   - curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
> - проверить версию можно командой minikube version
> - переключаемся на root и запускаем миникуб: minikube start --vm-driver=none
> - после запуска стоит проверить статус: minikube status
> - запущенные служебные компоненты можно увидеть командой: kubectl get pods --namespace=kube-system
>
> ### Для сброса кластера стоит удалить кластер и создать заново:
> - minikube delete
> - minikube start --vm-driver=none
>
> Возможно, для повторного запуска потребуется выполнить команду: sudo sysctl fs.protected_regular=0
>
> Инструкция по установке Minikube - [ссылка](https://kubernetes.io/ru/docs/tasks/tools/install-minikube/)
>
> **Важно**: t3.small не входит во free tier, следите за бюджетом аккаунта и удаляйте виртуалку.

Я решил установить на обычную вирт. машину.



| Описание действия                              | Команды                                                      |
| ---------------------------------------------- | ------------------------------------------------------------ |
| **Установка Minikube с помощью прямой ссылки** | **curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \<br/>  && chmod +x minikube<br/>sudo mkdir -p /usr/local/bin/<br/>sudo install minikube /usr/local/bin/  --verbose <br/>sudo yum install -y conntrack** |
| **Запускает локальный кластер Kubernetes**     | **minikube start --vm-driver=none**   #для Docker            |
| **Проверка состояния кластера**                | **minikube status**<br/>*minikube<br/>type: Control Plane<br/>host: Running<br/>kubelet: Running<br/>apiserver: Running<br/>kubeconfig: Configured* |



> ## Задача 2: Запуск Hello World
>
> После установки Minikube требуется его проверить. Для этого подойдет стандартное приложение hello world. А для доступа к нему потребуется ingress.
>
> - развернуть через Minikube тестовое приложение по [туториалу](https://kubernetes.io/ru/docs/tutorials/hello-minikube/#%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BA%D0%BB%D0%B0%D1%81%D1%82%D0%B5%D1%80%D0%B0-minikube)
> - установить аддоны ingress и dashboard
>

| Описание действия                                            | Команды                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Установить аддоны ingress и dashboard**                    | **minikube addons list<br/>minikube addons enable ingress<br/>minikube addons enable dashboard** |
| **создание деплоймента для управления подом c контейнером "Hello World"** | **kubectl create deployment hello-node --image=k8s.gcr.io/echoserver:1.4** |
| **Сделать Pod доступным для публичной сети**                       | **kubectl expose deployment hello-node --type=LoadBalancer --port=8080** |
| **Посмотреть  созданный сервис**                             | **kubectl get services**<br/>*hello-node   LoadBalancer   10.107.241.53   <pending>     8080:31376/TCP   72s<br/>kubernetes   ClusterIP      10.96.0.1       <none>        443/TCP          3h31m* |
| **Сделать сервис доступным (через LoadBalancer) при обращении с помощью команды** | **minikube service hello-node** <br/>*http://192.168.80.98:30988 * |

  Вывод kubectl get services:
| NAMESPACE |    NAME    | TARGET PORT |            URL             |
|-----------|------------|-------------|----------------------------|
| default   | hello-node |        8080 | http://192.168.80.98:30988 |



> ## Задача 3: Установить kubectl
>
>
> Подготовить рабочую машину для управления корпоративным кластером. Установить клиентское приложение kubectl.
> - подключиться к minikube 
> 
>-  проверить работу приложения из задания 2, запустив port-forward до кластера

  

  

  | Описание действия                                            | Команды                                                      |
  | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | Загрузить последнюю версию                                   | curl -LO https://storage.googleapis.com/kubernetes-release/release/\`curl -s    https://storage.googleapis.com/kubernetes-release/release/stable.txt\`/bin/linux/amd64/kubectl |
  | Делаем исполняемой                                           | **chmod +x ./kubectl**                                       |
  | Переместить двоичный файл в директорию из переменной окружения PATH | **sudo mv ./kubectl /usr/local/bin/kubectl**          |
  | Смотрим  версию:                                             | **kubectl version --client**                                 |
  | Для kubectl port-forward ставим socat                        | **yum install socat**                                        |
  | Посмотреть информацию о поде                                 | **kubectl get pods**  имя : hello-node-7567d9fdc9-lfhkq      |  
  | Делаем проброс до кластера через  kubectl port-forward       | **kubectl port-forward hello-node-7567d9fdc9-lfhkq 8080:8080**  |  

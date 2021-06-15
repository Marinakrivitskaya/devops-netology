> # Домашнее задание к занятию "12.4 Развертывание кластера на собственных серверах, лекция 2"
> Новые проекты пошли стабильным потоком. Каждый проект требует себе несколько кластеров: под тесты и продуктив. Делать все руками — не вариант, поэтому стоит автоматизировать подготовку новых кластеров.
>
> ## Задание 1: Подготовить инвентарь kubespray
> Новые тестовые кластеры требуют типичных простых настроек. Нужно подготовить инвентарь и проверить его работу. Требования к инвентарю:
> * подготовка работы кластера из 5 нод: 1 мастер и 4 рабочие ноды;
> * в качестве CRI — containerd;
> * запуск etcd производить на мастере.
>





| Установка Kubespray                      |                                                              |
| ---------------------------------------- | ------------------------------------------------------------ |
| Устанавливаем клиент Git                 | sudo yum install git -y                                      |
| Клонируем репозиторий                    | git clone  https://github.com/kubernetes-sigs/kubespray.git     cd kubespray |
| установить Ansible и другие зависимости. | sudo yum install python3-pip<br/>sudo pip3 install -r requirements.txt |



**~/kubespray/inventory/inventory.ini**

```
"[all]
node1 ansible_host=192.168.80.221 ip=192.168.80.221
node2 ansible_host=192.168.80.222 ip=192.168.80.222
node3 ansible_host=192.168.80.223 ip=192.168.80.223
node4 ansible_host=192.168.80.224 ip=192.168.80.224
node5 ansible_host=192.168.80.225 ip=192.168.80.225

[kube_control_plane]
 node1

[etcd]
 node1


[kube_node]
 node2
 node3
 node4
 node5

[k8s_cluster:children]
kube_control_plane
kube_node"

```

Согласно документации, пришлось поменять настройки для работы containerd.
https://github.com/kubernetes-sigs/kubespray/blob/master/docs/containerd.md

~ kubespray/inventory/group_vars/k8s_cluster/k8s_cluster.yml

```
container_manager: containerd
```

~kubespray/inventory/group_vars/all/etcd.yml

```
etcd_deployment_type: host
```

kubespray/inventory/group_vars/all/containerd.yml

```
containerd_registries:
  "docker.io":
    - "https://mirror.gcr.io"
    - "https://registry-1.docker.io"
```

Запускаем

```
ansible-playbook -u vagrant -i kubespray/inventory/inventory.ini -b --diff kubespray/cluster.yml --ask-pass
```



![](https://github.com/syatihoko/devops-netology/blob/master/HomeWorks4/12.4_Kubespray.jpg)



> ## Задание 2 (*): подготовить и проверить инвентарь для кластера в AWS
> Часть новых проектов хотят запускать на мощностях AWS. Требования похожи:
> * разворачивать 5 нод: 1 мастер и 4 рабочие ноды;
> * работать должны на минимально допустимых EC2 — t3.small.
>






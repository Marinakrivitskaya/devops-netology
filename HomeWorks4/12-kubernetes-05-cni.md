# Домашнее задание к занятию "12.5 Сетевые решения CNI"
После работы с Flannel появилась необходимость обеспечить безопасность для приложения. Для этого лучше всего подойдет Calico.
> ## Задание 1: установить в кластер CNI плагин Calico
> Для проверки других сетевых решений стоит поставить отличный от Flannel плагин — например, Calico. Требования: 
> * установка производится через ansible/kubespray;
> * после применения следует настроить политику доступа к hello world извне.
>



|                                                              |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Создаем  Deployment по умолчанию с 1 pod                     | kubectl create deployment hello-node  --image=k8s.gcr.io/echoserver:1.4 |
| Делаем доступным для публичной сети (создается объект сервис) | kubectl expose  deployment hello-node --type=LoadBalancer --port=8080 |
| Увеличиваем в deployment кол-во pods до 2                    | kubectl scale  deployments/hello-node --replicas=2           |

Попробовал создать политику Calico: 

**calico_hello-node.yml**

```
apiVersion: crd.projectcalico.org/v1
kind: NetworkPolicy
metadata:
  name: allow-hello-node
spec:
  ingress:
  - action: Allow
    protocol: TCP
    destination:
     Selector: app = 'hello-node'
      ports:
      - 6443
```

**[vagrant@node1 calico]$kubectl apply -f calico_hello-node.yml**

**[vagrant@node1 calico]$ calicoctl get networkPolicy**

```
NAME
allow-hello-node
```



> ## Задание 2: изучить, что запущено по умолчанию
> Самый простой способ — проверить командой calicoctl get <type>. Для проверки стоит получить список нод, ipPool и profile.
> Требования: 
>
> * установить утилиту calicoctl;
> * получить 3 вышеописанных типа в консоли.
>

calicoctl; - ставится по умолчанию через ansible/kubespray, если не выбирать другой плагин.

или установка сводится к применению файла calico.yaml, скачанного с официального сайта, с помощью **kubectl apply -f calico.yaml,** 

 **список нод**

```
[vagrant@node1 calico]$ calicoctl get node
NAME
node1
node2
node3
node4
node5
```

**ipPool** 

```
[vagrant@node1 calico]$ calicoctl get ippool
NAME           CIDR             SELECTOR
default-pool   10.233.64.0/18   all()
```

**ipPool**

```
[vagrant@node1 calico]$ calicoctl get ippool
NAME           CIDR             SELECTOR
default-pool   10.233.64.0/18   all()
```



**profile**

```
[vagrant@node1 calico]$ calicoctl get profile
NAME
projectcalico-default-allow
kns.default
kns.kube-node-lease
kns.kube-public
kns.kube-system
ksa.default.default
ksa.kube-node-lease.default
ksa.kube-public.default
ksa.kube-system.attachdetach-controller
ksa.kube-system.bootstrap-signer
ksa.kube-system.calico-kube-controllers
ksa.kube-system.calico-node
ksa.kube-system.certificate-controller
ksa.kube-system.clusterrole-aggregation-controller
ksa.kube-system.coredns
ksa.kube-system.cronjob-controller
ksa.kube-system.daemon-set-controller
ksa.kube-system.default
ksa.kube-system.deployment-controller
ksa.kube-system.disruption-controller
ksa.kube-system.dns-autoscaler
ksa.kube-system.endpoint-controller
ksa.kube-system.endpointslice-controller
ksa.kube-system.endpointslicemirroring-controller
ksa.kube-system.ephemeral-volume-controller
ksa.kube-system.expand-controller
ksa.kube-system.generic-garbage-collector
ksa.kube-system.horizontal-pod-autoscaler
ksa.kube-system.job-controller
ksa.kube-system.kube-proxy
ksa.kube-system.namespace-controller
ksa.kube-system.node-controller
ksa.kube-system.nodelocaldns
ksa.kube-system.persistent-volume-binder
ksa.kube-system.pod-garbage-collector
ksa.kube-system.pv-protection-controller
ksa.kube-system.pvc-protection-controller
ksa.kube-system.replicaset-controller
ksa.kube-system.replication-controller
ksa.kube-system.resourcequota-controller
ksa.kube-system.root-ca-cert-publisher
ksa.kube-system.service-account-controller
ksa.kube-system.service-controller
ksa.kube-system.statefulset-controller
ksa.kube-system.token-cleaner
ksa.kube-system.ttl-after-finished-controller
ksa.kube-system.ttl-controller
```


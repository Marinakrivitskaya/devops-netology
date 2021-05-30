> # Домашнее задание к занятию "12.2 Команды для работы с Kubernetes"
> Кластер — это сложная система, с которой крайне редко работает один человек. Квалифицированный devops умеет наладить работу всей команды, занимающейся каким-либо сервисом.
> После знакомства с кластером вас попросили выдать доступ нескольким разработчикам. Помимо этого требуется служебный аккаунт для просмотра логов.
>
> ## Задание 1: Запуск пода из образа в деплойменте
> Для начала следует разобраться с прямым запуском приложений из консоли. Такой подход поможет быстро развернуть инструменты отладки в кластере. Требуется запустить деплоймент на основе образа из hello world уже через deployment. Сразу стоит запустить 2 копии приложения (replicas=2). 
>
> Требования:
>  * пример из hello world запущен в качестве deployment
>  * количество реплик в deployment установлено в 2
>  * наличие deployment можно проверить командой kubectl get deployment
>  * наличие подов можно проверить командой kubectl get pods
>



| Действие                                                     | Команда                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Создаем Deployment по умолчанию с 1 pod                      | k**ubectl create  deployment hello-node --image=k8s.gcr.io/echoserver:1.4** |
| Делаем доступным для публичной сети (создается объект сервис) | k**ubectl expose  deployment hello-node --type=LoadBalancer --port=8080** |
| Посмотреть только что созданный сервис                       | **kubectl  get services** <br>*NAME      TYPE      CLUSTER-IP   EXTERNAL-IP  PORT(S)     AGE   <br/>  hello-node  LoadBalancer  10.111.139.17  <pending>   8080:31968/TCP  26s     <br/>kubernetes   ClusterIP   10.96.0.1    <none>    443/TCP     19d* |
| Узнайте URL-адрес открытого (exposed) сервиса                | **minikube service  hello-node --url**                       |
| Смотрим  deployment                                          | **kubectl  get deployments**    <br> *NAME      READY  UP-TO-DATE  AVAILABLE   AGE <br/>    hello-node  1/1   1      1      19m* |
| Смотрим pods                                                 | **kubectl  get pods**    <br> NAME             READY  STATUS    RESTARTS  AGE     hello-node-7567d9fdc9-lfhkq   1/1   Running  1       19m |
| Увеличиваем в deployment кол-во pods до 2                    | **kubectl scale  deployments/hello-node --replicas=2**       |
| Смотрим  deployment                                          | **kubectl  get deployments**    <br> NAME      READY  UP-TO-DATE  AVAILABLE   AGE  <br/>   hello-node  2/2   2      2      79m |
| Смотрим pods                                                 | **kubectl  get pods**    <br>  *NAME             READY  STATUS    RESTARTS  AGE     <br/>hello-node-7567d9fdc9-2j5nk   1/1   Running  0       79m     hello-node-7567d9fdc9-p22pc   1/1   Running  0       2m31s* |



>
> ## Задание 2: Просмотр логов для разработки
> Разработчикам крайне важно получать обратную связь от штатно работающего приложения и, еще важнее, об ошибках в его работе. 
> Требуется создать пользователя и выдать ему доступ на чтение конфигурации и логов подов в app-namespace.
>
> Требования: 
>  * создан новый токен доступа для пользователя
>  * пользователь прописан в локальный конфиг (~/.kube/config, блок users)
>  * пользователь может просматривать логи подов и их конфигурацию (kubectl logs pod <pod_id>, kubectl describe pod <pod_id>)
>

| Создание учетной записи                         |                                                              |
| ----------------------------------------------- | ------------------------------------------------------------ |
| Просмотр пространств имен                       | **#kubectl get  namespace**    <br> *NAME          STATUS  AGE     <br/>default        Active  19d    <br/> ingress-nginx     Active  19d* |
| Создание учетной записи службы      (вариант 1) | **cat <<EOF \| kubectl apply  -f -     <br/>apiVersion: v1     <br/>kind: ServiceAccount    <br/> metadata: <br/>     name: netology-ro <br/>     namespace:  default     <br/>EOF**     <br/>*serviceaccount/demo-user created* |
| Создание учетной записи службы      (вариант 2) | **kubectl create serviceaccount  netology-ro**               |
| Просмотр уч. Записи                             | **# kubectl  describe serviceaccount netology-ro**    <br/> *Name:        netology-ro     <br/>Namespace:      default    <br/> Labels:         <none>   <br/>  Annotations:      <none>   <br/>  Image pull secrets:   <none>  <br/>   Mountable secrets:   netology-ro-token-n85s4   <br/>  Tokens:         netology-ro-token-n85s4    <br/> Events:       <none>* |



| Создание роли                                                |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Проверить версии API для RBAC, доступные в кластере  Kubernetes: | **#kubectl api-versions\| grep rbac**      <br/>    rbac.authorization.k8s.io/v1rbac.authorization.k8s.io/v1beta1 |
| Cоздадим  роль, которая предоставит созданной учетной записи доступ читать логи и  смотреть конфигурацию подов. | **cat <<EOF \| kubectl apply -f -     <br/>kind: Role     apiVersion: rbac.authorization.k8s.io/v1     <br/>metadata:    <br/>  name: role-readlogpod    <br/>  namespace:  default     <br/>rules:     <br/>- apiGroups: ["", "extensions", "apps"]     <br/>   resources: ["pods","logs","pods/log"]   <br/>   verbs: ["get",  "list", "watch","describe",  "logs"]     <br/>EOF**     <br/>*role.rbac.authorization.k8s.io/role-readlogpod  created* |
| Проверить группу:                                            | # kubectl  get roles -n "default"     NAME         CREATED AT     role-readlogpod   2021-05-30T01:18:50Z |
|                                                              | kubectl  describe roles role-readlogpod                      |



| Получение токена   пользователя                              |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Проверьте имя токена  пользователя:                          | **kubectl describe sa netology-ro  -n default     <br/>***Name:          netology-ro     <br/>Namespace:      default     <br/>Labels:         <none>     <br/>Annotations:      <none>     <br/>Image pull secrets:   <none>     <br/>Mountable secrets:  netology-ro-token-n85s4     <br/>Tokens:         netology-ro-token-n85s4* |
| Получите  токен учетной записи службы, который будет использоваться для доступа к  Kubernetes на панели инструментов или через командную строку kubectl | **export  NAMESPACE="default"     <br/>export K8S_USER="netology-ro"    <br/>kubectl -n ${NAMESPACE} describe secret $(kubectl -n ${NAMESPACE} get  secret \| (grep ${K8S_USER} \|\| echo "$_") \| awk '{print $1}') \| grep  token: \| awk '{print $2}'\n** |
| Получите данные сертификата:                                 | **kubectl -n ${NAMESPACE} get secret `kubectl -n  ${NAMESPACE} get secret | (grep ${K8S_USER} || echo "$_") | awk  '{print $1}'` -o "jsonpath={.data['ca\.crt']}"** |
| Cмотрим секреты пользователя                                 | **kubectl describe secret netology-ro**                      |
| Если  нужно, можно сгенерировать дополнительные токены       | **kubectl apply -f -  <<EOF     <br/>apiVersion: v1     <br/>kind: Secret     <br/>metadata:      <br/>  name: netology-ro-new      <br/>  namespace:  ${NAMESPACE}      <br/>    annotations:        kubernetes.io/service-account.name: netology-ro     <br/>type: kubernetes.io/service-account-token     <br/>EOF** |
| Удалить  ненужный token                                      | **delete secret netology-ro-new**                            |



| Настройка конфига                               |                                                              |
| ----------------------------------------------- | ------------------------------------------------------------ |
| Добавляем  токен пользователя в конфиг          | **# kubectl config set-credentials netology-ro --token** <br/>*eyJhbGciOiJSUzI1NiIsImtpZCI6IlBwUkloTDhRcVEtMDgzaXpsVW1LOEot...* |
| Просмотр  текущего конфига                      | **cat ~/.kube/config**                                       |
| Смотрим  списк доступных контекстов             | **kubectl config  get-contexts    <br/>** *CURRENT   NAME    CLUSTER  AUTHINFO   NAMESPACE*    <br/>      *minikube  minikube   minikube  default* |
| Меняем у  текущего контекста пользователя       | **kubectl config set-context minikube --user netology-ro**     <br/>*Context "minikube" modified.* |
| Смотрим  списк доступных контекстов             | **# kubectl config  get-contexts** <br/>    CURRENT   NAME    CLUSTER  AUTHINFO   NAMESPACE  <br/>   *     minikube  minikube   netology-ro    default |
| Проверяем,  просмотр подов (есть доступ)        | **kubectl get pods**                                         |
| Посмотреть  Pod с его логами (есть доступ)      | **kubectl describe  pods/hello-node-7567d9fdc9-p22pc**       |
| Посмотреть  Logs Pod-a (есть доступ)            | **kubectl logs  pod/hello-node-7567d9fdc9-p22pc**            |
| Изменение  кол-ва реплик (нет доступа)          | **scale deployments/hello-node  --replicas=4**               |
| Удаление  Pod-а (нет доступа)                   | **kubectl delete  pods/hello-node-7567d9fdc9-2j5nk**         |
| Переключаемся  обратно на пользователя minikube | **kubectl config set-context  minikube --user minikube**     |





> 
>
>
> ## Задание 3: Изменение количества реплик 
> Поработав с приложением, вы получили запрос на увеличение количества реплик приложения для нагрузки. Необходимо изменить запущенный deployment, увеличив количество реплик до 5. Посмотрите статус запущенных подов после увеличения реплик. 
>
> Требования:
>  * в deployment из задания 1 изменено количество реплик на 5
>  * проверить что все поды перешли в статус running (kubectl get pods)
>



```
"Увеличиваем в deployment кол-во pods до 5
#kubectl scale deployments/hello-node --replicas=5"

#kubectl describe pod hello-node-7567d9fdc9-p22pc
#kubectl logs hello-node-7567d9fdc9-p22pc
#kubectl port-forward hello-node-7567d9fdc9-p22pc  8080:8080
"# kubectl get pod
NAME                          READY   STATUS    RESTARTS   AGE
hello-node-7567d9fdc9-2j5nk   1/1     Running   0          24h
hello-node-7567d9fdc9-48tw6   1/1     Running   0          38m
hello-node-7567d9fdc9-8jxzd   1/1     Running   0          38m
hello-node-7567d9fdc9-c6t5k   1/1     Running   0          38m
hello-node-7567d9fdc9-p22pc   1/1     Running   0          23h"
kubectl port-forward hello-node 8080:8080

```




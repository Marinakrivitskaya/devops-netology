# Домашнее задание к занятию "13.3 работа с kubectl"
## Задание 1: проверить работоспособность каждого компонента
> Для проверки работы можно использовать 2 способа: port-forward и exec. Используя оба способа, проверьте каждый компонент:
> * сделайте запросы к бекенду;
> * сделайте запросы к фронту;
> * подключитесь к базе данных.
>


================================================
**Бекенд exec:**   

**$ kubectl exec -it  backend-8dcf9b8c6-d957v -- curl localhost:9000;**   
*{"detail":"Not Found"}*      

================================================
**Бекен port-forward:**      

**[vagrant@node1 ~]$ kubectl port-forward pod/backend-8dcf9b8c6-d957v 9001:9000 &**    
*Forwarding from 127.0.0.1:9001 -> 9000*   
*Forwarding from [::1]:9001 -> 9000*   

*Handling connection for 9000*   #появилось при подключении.   


**[vagrant@node1 ~]$ curl localhost:9000**   
*{"detail":"Not Found"}*   



================================================
================================================
**Фронтенд exec:**   

**[kaa@kaacentos .kube]$ kubectl exec -it frontend-64dbfd6b94-cgr65 -- curl localhost:80**   

```   
<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Список</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="/build/main.css" rel="stylesheet">
</head>
<body>
    <main class="b-page">
        <h1 class="b-page__title">Список</h1>
        <div class="b-page__content b-items js-list"></div>
    </main>
    <script src="/build/main.js"></script>
</body>
```
================================================
**Фронтенд port-forward:**   

**[kaa@kaacentos .kube]$ kubectl port-forward pod/frontend-64dbfd6b94-cgr65 :80 &**   
*[1] 278535*   
*Forwarding from 127.0.0.1:33931 -> 80*   
*Forwarding from [::1]:33931 -> 8*   



**[kaa@kaacentos .kube]$ curl 127.0.0.1:33931**   

```
<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Список</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="/build/main.css" rel="stylesheet">
</head>
<body>
    <main class="b-page">
        <h1 class="b-page__title">Список</h1>
        <div class="b-page__content b-items js-list"></div>
    </main>
    <script src="/build/main.js"></script>
</body>

```



================================================
================================================
**БД Exec:**   

**[kaa@kaacentos .kube]$ kubectl exec -it db-0 -- psql -U postgres**   
*psql (13.3)*   
*Type "help" for help.*   

*postgres=#*   

================================================
**БД port-forward:**   

**[kaa@kaacentos ~]$ kubectl port-forward pod/db-0 :5432 &**      
*[2] 280907*   
*[kaa@kaacentos ~]$ Forwarding from 127.0.0.1:34133 -> 5432*   
*Forwarding from [::1]:34133 -> 5432*   



[kaa@kaacentos .kube]$ kubectl port-forward pod/db-0 :postgres &   

psql -c 'SELECT version()' -U postgres -h db news   



**[kaa@kaacentos ~]$ psql -c 'SELECT version()' -U postgres -h localhost -p 34133 news**   

*version*   

 *PostgreSQL 13.3 on x86_64-pc-linux-musl, compiled by gcc (Alpine 10.2.1_pre1) 10.2.1 20201203, 64-bit*   
*(1 row)*   





> ## Задание 2: ручное масштабирование
> При работе с приложением иногда может потребоваться вручную добавить пару копий. Используя команду kubectl scale, попробуйте увеличить количество бекенда и фронта до 3. После уменьшите количество копий до 1. Проверьте, на каких нодах оказались копии после каждого действия (kubectl describe).



***kubectl describe pods backend | grep "Node:  "**   
*Node:         node2/192.168.80.222*   

**kubectl describe pods frontend | grep "Node:  "**   
*Node:         node5/192.168.80.225*   

================================================

Масштабируем до 3 реплик   

**kubectl scale --replicas=3 deployment/backend**   

**kubectl scale --replicas=3 deployment/frontend**   

**kubectl describe pods backend | grep "Node: "**   
Node:         node2/192.168.80.222   
Node:         node2/192.168.80.222   
Node:         node5/192.168.80.225   



**kubectl describe pods frontend | grep "Node:  "**   

Node:         node4/192.168.80.224   
Node:         node5/192.168.80.225   
Node:         node3/192.168.80.223   


===============================================

Масштабируем до 1 реплик (обратно)  
**kubectl scale --replicas=1 deployment/backend**   

**kubectl describe pods backend | grep "Node: "**   

*Node:         node5/192.168.80.225*   



**kubectl scale --replicas=1 deployment/frontend**   

**kubectl describe pods frontend | grep "Node:  "**   

*Node:         node5/192.168.80.225*      




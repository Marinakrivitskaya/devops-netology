# Домашнее задание к занятию "10.03. Grafana"







> ## Обязательные задания
>
> ### Задание 1
> Используя директорию [help](./help) внутри данного домашнего задания - запустите связку prometheus-grafana.
>
> Зайдите в веб-интерфейс графана, используя авторизационные данные, указанные в манифесте docker-compose.
>
> Подключите поднятый вами prometheus как источник данных.
>
> Решение домашнего задания - скриншот веб-интерфейса grafana со списком подключенных Datasource.

 

**https://prnt.sc/z00akd**    



> 
>
> ## Задание 2
> Изучите самостоятельно ресурсы:
> - [promql-for-humans](https://timber.io/blog/promql-for-humans/#cpu-usage-by-instance)
> - [understanding prometheus cpu metrics](https://www.robustperception.io/understanding-machine-cpu-usage)
>
> Создайте Dashboard и в ней создайте следующие Panels:
> - Утилизация CPU для nodeexporter (в процентах, 100-idle)
> - CPULA 1/5/15
> - Количество свободной оперативной памяти
> - Количество места на файловой системе
>
> Для решения данного ДЗ приведите promql запросы для выдачи этих метрик, а также скриншот получившейся Dashboard.



**\>Утилизация** **CPU для** **nodeexporter (в процентах, 100-****idle)**    

**Metrics:** 100 - (avg by (instance) (rate(node_cpu_seconds_total{job="node",mode="idle"}[1m]))* 100)    

 

**\>CPULA 1/5/15 **   

**Metric1:** node_load1    

**Metric2:** node_load5  

**Metric 3:** node_load15

 

 

**\>Количество свободной оперативной памяти**

  **Metrics:** node_memory_MemFree_bytes/1024/1024

 

 

**>Количество места на файловой системе**     

**Metrics:  node_filesystem_avail_bytes{fstype!~"tmpfs|fuse.lxcfs|squashfs",mountpoint!="/boot",job="node"}** 

**Legent:** {{mountpoint}}

 

**\> скриншот получившейся Dashboard.**

https://prnt.sc/z8btfo



> ## Задание 3
> Создайте для каждой Dashboard подходящее правило alert (можно обратиться к первой лекции в блоке "Мониторинг").
>
> Для решения ДЗ - приведите скриншот вашей итоговой Dashboard.



**/>Настройки канала оповещения Email**    

https://prnt.sc/zkg0rk



```
/etc/grafana/custom.ini
#################################### SMTP / Emailing ##########################
[smtp]
enabled = true
host = mail.avisoftica.ru:587
user = alertmanager
# If the password contains # or ; you have to wrap it with triple quotes. Ex """#password;"""
password = XXXXXXXXXX
;cert_file =
;key_file =
skip_verify = true
from_address = alertmanager@avisoftica.ru
from_name = Grafana
# EHLO identity in SMTP dialog (defaults to instance_name)
ehlo_identity = kaa_conf2.avisoftica.ru
# SMTP startTLS policy (defaults to 'OpportunisticStartTLS')
;startTLS_policy = NoStartTLS
```



**/>Для решения ДЗ - приведите скриншот вашей итоговой Dashboard.**
https://prnt.sc/zko6lk





> ## Задание 4
> Сохраните ваш Dashboard.
>
> Для этого перейдите в настройки Dashboard, выберите в боковом меню "JSON MODEL".
>
> Далее скопируйте отображаемое json-содержимое в отдельный файл и сохраните его.
>
> В решении задания - приведите листинг этого файла.



**Dashboard_Netology.json** :







## Задание повышенной сложности

> **В части задания 1** не используйте директорию [help](./help) для сборки проекта, самостоятельно разверните grafana, где в 
> роли источника данных будет выступать prometheus, а сборщиком данных node-exporter:
>
> - grafana
> - prometheus-server
> - prometheus node-exporter
>
> За дополнительными материалами, вы можете обратиться в официальную документацию grafana и prometheus.
>
> В решении к домашнему заданию приведите также все конфигурации/скрипты/манифесты, которые вы 
> использовали в процессе решения задания.
>
> **В части задания 3** вы должны самостоятельно завести удобный для вас канал нотификации, например Telegram или Email
> и отправить туда тестовые события.
>
> В решении приведите скриншоты тестовых событий из каналов нотификаций.



**/>Оповещение по почте:**   
https://prnt.sc/zkwx1u   


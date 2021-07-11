> # Домашнее задание к занятию "13.4 инструменты для упрощения написания конфигурационных файлов. Helm и Jsonnet"
> В работе часто приходится применять системы автоматической генерации конфигураций. Для изучения нюансов использования разных инструментов нужно попробовать упаковать приложение каждым из них.
>
> ## Задание 1: подготовить helm чарт для приложения
> Необходимо упаковать приложение в чарт для деплоя в разные окружения. Требования:
> * каждый компонент приложения деплоится отдельным deployment’ом/statefulset’ом;
> * в переменных чарта измените образ приложения для изменения версии.
>

Версия1

```
helm package kaa-chart1
Successfully packaged chart and saved it to: /home/20210705-helm-chart1/kaa-chart1-0.1.0.tgz
```

Версия2

```
helm package kaa-chart1
Successfully packaged chart and saved it to: /home/20210705-helm-chart1/kaa-chart1-0.1.1.tgz
```

Версия3

```
helm package kaa-chart1
Successfully packaged chart and saved it to: /home/20210705-helm-chart1/kaa-chart1-0.1.2.tgz
```

Ссылка на chart в конце.

## Задание 2: запустить 2 версии в разных неймспейсах
Подготовив чарт, необходимо его проверить. Попробуйте запустить несколько копий приложения:
* одну версию в namespace=app1;
* вторую версию в том же неймспейсе;
* третью версию в namespace=app2.

```
# kubectl create namespace app1;
namespace/app1 created
# kubectl create namespace app2;
namespace/app2 created

```



Первая версия в app1

```
# helm install kaa-chart1v1 ./kaa-chart1-0.1.0.tgz --namespace app1
```

Вторая версия в app1

```
# helm install kaa-chart1v2 ./kaa-chart1-0.1.1.tgz --namespace app1
Error: rendered manifests contain a resource that already exists. Unable to continue with install: Service "backend" in namespace "app1" exists and cannot be imported into the current release: invalid ownership metadata; annotation validation error: key "meta.helm.sh/release-name" must equal "kaa-chart1v2": current value is "kaa-chart1v1"
Комментарии преподавателя: нужно было изменить имя релиза через флаг --name.
```





Вторая версия в дефолтном

```
# helm install kaa-chart1v2 ./kaa-chart1-0.1.1.tgz
```

Третья версия в app2

```
# helm install kaa-chart1v3 ./kaa-chart1-0.1.2.tgz --namespace app2
```



Проверка работы: 

```
# kubectl get pods
NAME                       READY   STATUS    RESTARTS   AGE
backend-749b8cbf59-fr6vs   1/1     Running   0          113s
db-0                       1/1     Running   0          113s
frontend-89dc7d67f-g48zz   1/1     Running   0          113s
```



```
# kubectl get pods -n app1
NAME                        READY   STATUS    RESTARTS   AGE
backend-9684db5d7-npg7r     1/1     Running   0          5m54s
db-0                        1/1     Running   0          5m54s
frontend-6774cf6bf5-ps6m2   1/1     Running   0          5m54s
```



```
kubectl get pods -n app2
NAME                       READY   STATUS    RESTARTS   AGE
backend-6db495f487-r9ccn   1/1     Running   0          103s
db-0                       1/1     Running   0          103s
frontend-df5864587-4f4qk   1/1     Running   0          103s
```



Удаление:

```
# helm uninstall kaa-chart1v2
release "kaa-chart1v2" uninstalled
# helm uninstall kaa-chart1v1 -n app1
release "kaa-chart1v1" uninstalled
root@node1 20210705-helm-chart1]# helm uninstall kaa-chart1v3 -n app2
release "kaa-chart1v3" uninstalled
```

Единственное с чем столкнулся, это проблема порядка запуска подов, БД позже стартует, чем backend (для проверки работы deploy выставил в 0 и опять в 1.
Комментарий преподавателя: Для того, чтобы приложение не стартовало раньше базы можно добавить entrypoint скрипт, который будет проверять доступность базы и только после этого стартовать приложение.



Лог бекенда, после перезапуска

```
# kubectl logs backend-64f6859955-7dzql
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
INFO:     Started reloader process [7] using statreload
INFO:     Started server process [13]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Лог фронта

```
# kubectl logs frontend-86586d949f-nltth
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: /etc/nginx/conf.d/default.conf differs from the packaged version
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2021/07/06 20:35:54 [notice] 1#1: using the "epoll" event method
2021/07/06 20:35:54 [notice] 1#1: nginx/1.21.0
2021/07/06 20:35:54 [notice] 1#1: built by gcc 8.3.0 (Debian 8.3.0-6)
2021/07/06 20:35:54 [notice] 1#1: OS: Linux 3.10.0-1160.25.1.el7.x86_64
2021/07/06 20:35:54 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2021/07/06 20:35:54 [notice] 1#1: start worker processes
2021/07/06 20:35:54 [notice] 1#1: start worker process 30
2021/07/06 20:35:54 [notice] 1#1: start worker process 31
```

Лог БД

```
....
PostgreSQL init process complete; ready for start up.

2021-07-06 20:36:18.427 UTC [1] LOG:  starting PostgreSQL 13.3 (Debian 13.3-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
2021-07-06 20:36:18.428 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2021-07-06 20:36:18.428 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2021-07-06 20:36:18.447 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2021-07-06 20:36:18.451 UTC [75] LOG:  database system was shut down at 2021-07-06 20:36:18 UTC
2021-07-06 20:36:18.454 UTC [1] LOG:  database system is ready to accept connections

```





Ссылка на chart: https://github.com/kaa-kubernetes/20210705-helm-chart1/tree/master/kaa-chart1

(не менял NOTES.txt)



> ## Задание 3 (*): повторить упаковку на jsonnet
> Для изучения другого инструмента стоит попробовать повторить опыт упаковки из задания 1, только теперь с помощью инструмента jsonnet.

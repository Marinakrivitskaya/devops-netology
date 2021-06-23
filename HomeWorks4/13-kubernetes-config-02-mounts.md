> # Домашнее задание к занятию "13.2 разделы и монтирование"
> Приложение запущено и работает, но время от времени появляется необходимость передавать между бекендами данные. А сам бекенд генерирует статику для фронта. Нужно оптимизировать это.
> Для настройки NFS сервера можно воспользоваться следующей инструкцией (производить под пользователем на сервере, у которого есть доступ до kubectl):
> * установить helm: curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
> * добавить репозиторий чартов: helm repo add stable https://charts.helm.sh/stable && helm repo update
> * установить nfs-server через helm: helm install nfs-server stable/nfs-server-provisioner
>
> В конце установки будет выдан пример создания PVC для этого сервера.
>

> ## Задание 1: подключить для тестового конфига общую папку
> В stage окружении часто возникает необходимость отдавать статику бекенда сразу фронтом. Проще всего сделать это через общую папку. Требования:
> * в поде подключена общая папка между контейнерами (например, /static);
> * после записи чего-либо в контейнере с беком файлы можно получить из контейнера с фронтом.
>



Создаем PVC  от nfs:

**#kubectl apply -f nfs_pvc.yml**

```
---
    kind: PersistentVolumeClaim
    apiVersion: v1
    metadata:
      name: test-dynamic-volume-claim
    spec:
      storageClassName: "nfs"
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 100Mi

```

Создаем deployment  c nfs:

**#kubectl apply -f deployment_with_nfs.yml**

```
---
apiVersion: apps/v1
kind: Deployment
metadata:
    name: nfs-deployment
spec:
    replicas: 1
    selector:
        matchLabels:
            app: test
    template:
        metadata:
            labels:
                app: test
        spec:
            containers:
            - image: nginx:latest
              name: test-0
              volumeMounts:
              - mountPath: /static
                name: test-pv-storage
            - image: bitnami/php-fpm:latest
              name: test-1
              volumeMounts:
              - mountPath: /static
                name: test-pv-storage
            volumes:.
            - name: test-pv-storage
              persistentVolumeClaim:
                  claimName: test-dynamic-volume-claim
```

Смотрим, что директория общая: 

**kubectl exec -it nfs-deployment-85c6f67487-f2h6s  -c test-0 bash**

**cd /static/   
echo test > static_file  **

**kubectl exec -it nfs-deployment-85c6f67487-f2h6s  -c test-1 bash**

**cd /static/    
echo static_file   **



Или Pod  c nfs:

**kubectl apply -f  pod_with_nfs.yml**

```
---
apiVersion: v1
kind: Pod
metadata:
    name: test-pd-pv
spec:
    containers:
        - image: nginx:latest
          name: test-0
          volumeMounts:
          - mountPath: /static
            name: test-pv-storage
        - image: bitnami/php-fpm:latest
          name: test-1
          volumeMounts:
          - mountPath: /static
            name: test-pv-storage
    volumes:
        - name: test-pv-storage
          persistentVolumeClaim:
              claimName: test-dynamic-volume-claim
```

Смотрим, что директория общая: 

**kubectl exec -it test-pd-pv -c test-0 bash**

cd /static/
echo test > static_file

**kubectl exec -it test-pd-pv -c test-1 bash**

cd /static/
echo static_file





> ## Задание 2: подключить общую папку для прода
> Поработав на stage, доработки нужно отправить на прод. В продуктиве у нас контейнеры крутятся в разных подах, поэтому потребуется PV и связь через PVC. Сам PV должен быть связан с NFS сервером. Требования:
> * все бекенды подключаются к одному PV в режиме ReadWriteMany;
> * фронтенды тоже подключаются к этому же PV с таким же режимом;
> * файлы, созданные бекендом, должны быть доступны фронту.
>

Здесь разделим Deployment на 2, по 1 контейнеру

**#kubectl apply -f deployment_with_nfs1.yml** 

```
---
apiVersion: apps/v1
kind: Deployment
metadata:
    name: nfs-deployment1
spec:
    replicas: 1
    selector:
        matchLabels:
            app: test
    template:
        metadata:
            labels:
                app: test
        spec:
            containers:
            - image: nginx:latest
              name: test-0
              volumeMounts:
              - mountPath: /static
                name: test-pv-storage
            volumes:.
            - name: test-pv-storage
              persistentVolumeClaim:
                  claimName: test-dynamic-volume-claim
```



**#kubectl apply -f deployment_with_nfs2.yml** 

На втором добавляем readonly, так как ему нужно только читать, не писать на диск.

```
---
apiVersion: apps/v1
kind: Deployment
metadata:
    name: nfs-deployment2
spec:
    replicas: 1
    selector:
        matchLabels:
            app: test
    template:
        metadata:
            labels:
                app: test
        spec:
            containers:
            - image: bitnami/php-fpm:latest
              name: test-1
              volumeMounts:
              - mountPath: /static
                name: test-pv-storage
            volumes:
            - name: test-pv-storage
              persistentVolumeClaim:
                  claimName: test-dynamic-volume-claim
                  readOnly: true
```



Также по идее нужно было бы переключить PVC на  *ReadWriteMany*, но наверное особенность NFS в том, что и при режиме *ReadWriteOnce* могут писать\читать несколько подов одновременно. 

# Домашнее задание к занятию "13.1 контейнеры, поды, deployment, statefulset, services, endpoints"
Настроив кластер, подготовьте приложение к запуску в нём. 
Приложение стандартное: бекенд, фронтенд, база данных (пример можно найти в папке 13-kubernetes-config).

> ## Задание 1: подготовить тестовый конфиг для запуска приложения
> Для начала следует подготовить запуск приложения в stage окружении с простыми настройками. Требования:
> * под содержит в себе 3 контейнера — фронтенд, бекенд, базу;
> * регулируется с помощью deployment фронтенд и бекенд;
> * база данных — через statefulset.
>



из Docker-файлов - фронтенд, бекенд-а сделал свои images.

Получившийся Deployment:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    netology.service: frontend-backend
  name: frontend-backend
spec:
  replicas: 1
  selector:
    matchLabels:
      netology.service: frontend-backend
  strategy: {}
  template:
    metadata:
      labels:
        netology.service: frontend-backend
    spec:
      containers:
        - image: kaaa/13_1_front:latest
          name: frontend
          ports:
            - containerPort: 80
          resources: {}
        - image: kaaa/13_1_backend:latest
          name: backend  
          env:
            - name: DATABASE_URL
              value: postgres://postgres:postgres@db:5432/news
          ports:
            - containerPort: 9000
          resources: {}
      restartPolicy: Always

```

Получившийся StatefulSet для БД:

```
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: "postgesql"
  replicas: 1
  selector:
    matchLabels:
      netology.service: db
  template:
    metadata:
      labels:
        netology.service: db
    spec:
      containers:
        - image: postgres:13-alpine
          name: db
          env:
            - name: POSTGRES_DB
              value: news
            - name: POSTGRES_PASSWORD
              value: postgres
            - name: POSTGRES_USER
              value: postgres
```



> ## Задание 2: подготовить конфиг для продуктива
> Следующим шагом будет запуск приложения в production окружении. Требования сложнее:
> * каждый компонент (база, бекенд, фронтенд) запускаются в своем поде, регулируются отдельными deployment’ами;
> * для связи используются service (у каждого компонента свой);
> * в окружении фронта прописан адрес сервиса бекенда;
> * в окружении бекенда прописан адрес сервиса базы данных.
>



**база**

```
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  serviceName: "postgesql"
  replicas: 1
  selector:
    matchLabels:
      netology.service: db
  template:
    metadata:
      labels:
        netology.service: db
    spec:
      containers:
        - image: postgres:13-alpine
          name: db
          env:
            - name: POSTGRES_DB
              value: news
            - name: POSTGRES_PASSWORD
              value: postgres
            - name: POSTGRES_USER
              value: postgres

```

**база_сервис**

```
---
apiVersion: v1
kind: Service
metadata:
  annotations:
  creationTimestamp: null
  labels:
    netology.service: db
  name: db
spec:
  ports:
    - name: "8080"
      port: 5432
      targetPort: 5432
  selector:
    netology.service: db
  type: ClusterIP
```

**бекенд**

```
---
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    netology.service: backend
  name: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      netology.service: backend
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        netology.service: backend
    spec:
      containers:
        - image: kaaa/13_1_backend:latest
          name: backend..
          env:
            - name: DATABASE_URL
              value: postgres://postgres:postgres@db:5432/news   #db = 10.233.7.17
          ports:
            - containerPort: 9000
          resources: {}
      restartPolicy: Always
status: {}

```

**бекенд-сервис  **  #kubectl apply -f service_backend.yml

```
---
apiVersion: v1
kind: Service
metadata:
  labels:
    netology.service: backend
  name: backend
spec:
  ports:
    - name: "9000"
      port: 9000
      targetPort: 9000
  selector:
    netology.service: backend
  type: LoadBalancer
status:
  loadBalancer: {}
```

**фронтенд**

```
---
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    netology.service: frontend
  name: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      netology.service: frontend
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        netology.service: frontend
    spec:
      containers:
        - image: kaaa/13_1_front:latest
          name: frontend
          ports:
            - containerPort: 80
          env:
            - name: BASE_URL
              value: http://backend:32669  # backend:32669 = 10.233.36.252:32669 => 9000     
          resources: {}
      restartPolicy: Always
status: {}
```

**фронтенд-сервис**

```
---
apiVersion: v1
kind: Service
metadata:
  annotations:
  creationTimestamp: null
  labels:
    netology.service: frontend
  name: frontend
spec:
  ports:
    - name: "8080"
#      nodePort:   #The range of valid ports is 30000-32767
      port: 8000
      targetPort: 80
  selector:
    netology.service: frontend
  type: LoadBalancer
status:
  loadBalancer: {}
```

**$ kubectl get services**

```
NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
backend      LoadBalancer   10.233.36.252   <pending>     9000:32669/TCP   12m
db           ClusterIP      10.233.7.17     <none>        5432/TCP         8s
frontend     LoadBalancer   10.233.3.213    <pending>     8000:31320/TCP   13m
kubernetes   ClusterIP      10.233.0.1      <none>        443/TCP          6d23h
```



> ## Задание 3 (*): добавить endpoint на внешний ресурс api
> Приложению потребовалось внешнее api, и для его использования лучше добавить endpoint в кластер, направленный на это api. Требования:
> * добавлен endpoint до внешнего api (например, геокодер).
>

Попробовал создать,  но наверное не в ту сторону пошел, ExternalName имеет проблемы по работе через HTTPS

```
---
kind: Service
apiVersion: v1
metadata:
  name: external-svc-gis
spec:
  type: ExternalName
  externalName: catalog.api.2gis.com
```

Если бы протокол был не https, то наверное можно было, что то вроде этого сделать:

```
---
kind: Service
apiVersion: v1
metadata:
  name: external-svc
spec:
  ports:
    - name: web
      protocol: TCP
      port: 80
      targetPort: 80"
---
kind: Endpoints
apiVersion: v1
metadata:
  name: external-svc
subsets: 
  - addresses:
        - ip: 139.59.205.180
    ports:
      - port: 80
        name: web"

```


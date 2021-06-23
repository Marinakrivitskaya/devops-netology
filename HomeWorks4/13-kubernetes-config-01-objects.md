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

**#kubectl apply -f deployment_front_back.yml**

```
---
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
      restartPolicy: Always
```

Получившийся StatefulSet для БД:

**#kubectl apply -f StatefulSet_db.yml**

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

**Сервис для БД:**

**#kubectl apply -f service_bd.yml**

```
---
apiVersion: v1
kind: Service
metadata:
  annotations:
  labels:
    netology.service: db
  name: db
spec:
  ports:
    - name: "postgresql"
      port: 5432
      targetPort: 5432
  selector:
    netology.service: db
  type: ClusterIP
```

> ## Задание 2: подготовить конфиг для продуктива
> Следующим шагом будет запуск приложения в production окружении. Требования сложнее:
> * каждый компонент (база, бекенд, фронтенд) запускаются в своем поде, регулируются отдельными deployment’ами;
> * для связи используются service (у каждого компонента свой);
> * в окружении фронта прописан адрес сервиса бекенда;
> * в окружении бекенда прописан адрес сервиса базы данных.
>



**База данных**
**#kubectl apply -f StatefulSet_db.yml**

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

**Сервис для БД**

**#kubectl apply -f service_bd.yml**

```
---
apiVersion: v1
kind: Service
metadata:
  annotations:
  labels:
    netology.service: db
  name: db
spec:
  ports:
    - name: "postgresql"
      port: 5432
      targetPort: 5432
  selector:
    netology.service: db
  type: ClusterIP
```

**Бекенд**

**#kubectl apply -f deployment_back.yml**
```
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    netology.service: backend
  name: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      netology.service: backend
  template:
    metadata:
      labels:
        netology.service: backend
    spec:
      containers:
        - image: kaaa/13_1_backend:latest
          name: backend
          env:
            - name: DATABASE_URL
              value: postgres://postgres:postgres@db:5432/news
          ports:
            - containerPort: 9000
      restartPolicy: Always
```

**Сервис для Бекенда** 
**#kubectl apply -f service_backend.yml**
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
    - name: "backend-port"
      port: 9000
      targetPort: 9000
  selector:
    netology.service: backend
  type: ClusterIP
```

**Фронтенд**
**#kubectl apply -f deployment_front.yml**

```
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    netology.service: frontend
  name: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      netology.service: frontend
  template:
    metadata:
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
              value: http://backend:9000
      restartPolicy: Always
```

**Сервис для Фронтенд**
**#kubectl apply -f service_frontend.yml**
```
---
apiVersion: v1
kind: Service
metadata:
  annotations:
  labels:
    netology.service: frontend
  name: frontend
spec:
  ports:
    - name: "frontend-port"
      port: 8000
      targetPort: 80
  selector:
    netology.service: frontend
  type: ClusterIP
```

**$ kubectl get services**

![](https://github.com/syatihoko/devops-netology/blob/master/HomeWorks4/services.jpg)  

**$kubectl get pods**   

![](https://github.com/syatihoko/devops-netology/blob/master/HomeWorks4/pods.jpg)

**$ kubectl get statefulset**

![](https://github.com/syatihoko/devops-netology/blob/master/HomeWorks4/statefulset.jpg)

**$ kubectl get deploy**

![](https://github.com/syatihoko/devops-netology/blob/master/HomeWorks4/deploy.jpg)


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
selector: {}
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


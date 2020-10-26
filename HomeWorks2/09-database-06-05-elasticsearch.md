> ## Задача 1
>
> В этом задании вы потренируетесь в:
>
> - установке     elasticsearch
> - первоначальном     конфигурировании elastcisearch
> - запуске     elasticsearch в docker
>
> Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и [документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):
>
> - составьте     Dockerfile-манифест для elasticsearch
> - соберите     docker-образ и сделайте `push` в     ваш docker.io репозиторий
> - запустите     контейнер из получившегося образа и выполните запрос пути `/` c хост-машины
>
> Требования к `elasticsearch.yml`:
>
> - данные `path` должны сохраняться в `/var/lib`
> - имя     ноды должно быть `netology_test`
>
> В ответе приведите:
>
> - текст     Dockerfile манифеста
> - ссылку     на образ в репозитории dockerhub
> - ответ `elasticsearch` на запрос пути `/` в json виде
>
> Подсказки:
>
> - возможно     вам понадобится установка пакета perl-Digest-SHA для корректной работы     пакета shasum
> - при     сетевых проблемах внимательно изучите кластерные и сетевые настройки в     elasticsearch.yml
> - при     некоторых проблемах вам поможет docker директива ulimit
> - elasticsearch     в логах обычно описывает проблему и пути ее решения
>
> Далее мы будем работать с данным экземпляром elasticsearch.



> текст Dockerfile манифеста

```
FROM centos:7

 

LABEL Andrey K. kaa.a.a@mail.ru

 

 

RUN yum install -y wget

#Скачиваем дистрибутив

RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.9.3-linux-x86_64.tar.gz

 

#распаковываем в/var/lib/

RUN tar -xzf elasticsearch-7.9.3-linux-x86_64.tar.gz -C /var/lib/

 

#Удаляем архив

RUN rm -f elasticsearch-7.9.3-linux-x86_64.tar.gz

 
#Устанавливаем переменную домашней директории ES - ES_HOME

ENV ES_HOME /var/lib/elasticsearch-7.9.3

 

#Добавляем пользователя (elasticsearch\java не работает из-под root)

#Даем права пользователю

RUN groupadd --gid 2000 elasticsearch \

 && useradd --uid 2000 --gid elasticsearch --shell /bin/bash --create-home elasticsearch \

 && chown elasticsearch:elasticsearch -R $ES_HOME

 

#Меняем пользователя на elasticsearch

USER 2000

 

#Устанавливаем переменную домашней директории ES - ES_HOME повторно, так как пользователь изменился

ENV ES_HOME /var/lib/elasticsearch-7.9.3

 

#Переходим в директорию с программой

WORKDIR $ES_HOME

 

#определяет команду, которую нужно запустить для ES

ENTRYPOINT ["bin/elasticsearch"]

 

 

#Запускаем, не подходит как демон(-d -p pid), задаем имя ноды

CMD ["-Enode.name=netology_test"]


```



> ссылку на образ в репозитории dockerhub



https://hub.docker.com/repository/docker/kaaa/elastic



> ответ elasticsearch на запрос пути / в json виде



запускаем 

**#docker run -di kaaa/elastic**



**#docker exec 6d4fd169d9d1 curl -X GET 'localhost:9200/'**



```
 % Total  % Received % Xferd Average Speed  Time  Time   Time Current

​                 Dload Upload  Total  Spent  Left Speed

100  538 100  538  0   0 54201   0 --:--:-- --:--:-- --:--:-- 59777

{

 "name" : "netology_test",

 "cluster_name" : "elasticsearch",

 "cluster_uuid" : "u-1lX-63QPKmvHgVElfe6A",

 "version" : {

  "number" : "7.9.3",

  "build_flavor" : "default",

  "build_type" : "tar",

  "build_hash" : "c4138e51121ef06a6404866cddc601906fe5c868",

  "build_date" : "2020-10-16T10:36:16.141335Z",

  "build_snapshot" : false,

  "lucene_version" : "8.6.2",

  "minimum_wire_compatibility_version" : "6.8.0",

  "minimum_index_compatibility_version" : "6.0.0-beta1"

 },

 "tagline" : "You Know, for Search"
```







> 
>
> ##  Задача 2
>
> В этом задании вы научитесь:
>
> - создавать     и удалять индексы
> - изучать     состояние кластера
> - обосновывать     причину деградации доступности данных
>
> Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:
>
> | **Имя** | **Количество реплик** | **Количество шард** |
> | ------- | --------------------- | ------------------- |
> | ind-1   | 0                     | 1                   |
> | ind-2   | 1                     | 2                   |
> | ind-3   | 2                     | 4                   |
>
> Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.
>
> Получите состояние кластера `elasticsearch`, используя API.
>
> Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?
>
> Удалите все индексы.
>
> **Важно**
>
> При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард, иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.



> Получите список индексов и их статусов, используя API и приведите в ответе на задание.



Создаем индексы

**#curl -XPUT 'localhost:9200/ind-1' -H 'content-type: application/json' -d '{"settings": {"index": {"number_of_shards": 1,"number_of_replicas": 0}}}'**



**#curl -XPUT 'localhost:9200/ind-2' -H 'content-type: application/json' -d '{"settings": {"index": {"number_of_shards": 2,"number_of_replicas": 1}}}'**



**#curl -XPUT 'localhost:9200/ind-3' -H 'content-type: application/json' -d '{"settings": {"index": {"number_of_shards": 4,"number_of_replicas": 2}}}'**

 

**# curl 'localhost:9200/_cat/indices?v'**

```
health status index uuid          pri rep docs.count docs.deleted store.size pri.store.size

green open  ind-1 m9mSVhbNQT6yUuhfHYiQjw  1  0     0      0    208b      208b

yellow open  ind-3 oA11OEpSQjCUGhpu7hqtkA  4  2     0      0    832b      832b

yellow open  ind-2 Rg5zwrCuTvu24gZsWiJhVA  2  1     0      0    416b      416b
```



> Получите состояние кластера elasticsearch, используя API.

**# curl -XGET 'localhost:9200/_cluster/health?pretty'**

```
{

 "cluster_name" : "elasticsearch",

 "status" : "yellow",

 "timed_out" : false,

 "number_of_nodes" : 1,

 "number_of_data_nodes" : 1,

 "active_primary_shards" : 7,

 "active_shards" : 7,

 "relocating_shards" : 0,

 "initializing_shards" : 0,

 "unassigned_shards" : 10,

 "delayed_unassigned_shards" : 0,

 "number_of_pending_tasks" : 0,

 "number_of_in_flight_fetch" : 0,

 "task_max_waiting_in_queue_millis" : 0,

 "active_shards_percent_as_number" : 41.17647058823529
```





> Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

Для данных индексов установлено количество реплик отличное от 0 (что подразумевает наличие других узлов не меньше этого значения), но узел в кластере сейчас только один.

 

> Удалите все индексы.

**#curl -XDELETE localhost:9200/_all**







> ## Задача 3
>
> В данном задании вы научитесь:
>
> - создавать     бэкапы данных
> - восстанавливать     индексы из бэкапов
>
> Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.
>
> Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) данную директорию как `snapshot repository` c именем `netology_backup`.
>
> **Приведите в ответе** запрос API и результат вызова API для создания репозитория.
>
> 
>
> Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.
>
> [Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) состояния кластера `elasticsearch`.
>
> **Приведите в ответе** список файлов в директории со `snapshot`ами.
>
> Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.
>
> [Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние кластера `elasticsearch` из `snapshot`, созданного ранее.
>
> **Приведите в ответе** запрос к API восстановления и итоговый список индексов.
>
> Подсказки:
>
> - возможно     вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch```





**# docker exec -u root -ti 4fc75239c711 /bin/bash**



> Создайте директорию {путь до корневой директории с elasticsearch в образе}/snapshots.

**#mkdir $ES_HOME/snapshots**



> Используя API зарегистрируйте данную директорию как snapshot repository c именем netology_backup.
>
> Приведите в ответе запрос API и результат вызова API для создания репозитория.

 

**#echo path.repo: [ \"/var/lib/elasticsearch-7.9.3/snapshots\" ] >> "$ES_HOME/config/elasticsearch.yml"**

**#chown elasticsearch:elasticsearch /var/lib/elasticsearch-7.9.3/snapshots**

 

перезапустил Docker с elasticsearch

 

 

**#curl -XPUT 'localhost:9200/_snapshot/netology_backup' -H 'content-type: application/json' -d '{"type": "fs", "settings": {"location": "/var/lib/elasticsearch-7.9.3/snapshots"}}'**

*{"acknowledged":true}*



**#curl 'localhost:9200/_cat/indices?v'**

```
health status index uuid          pri rep docs.count docs.deleted store.size pri.store.size

green open  test ezwCooh_TaSuuhQDFs3png  1  0     0      0    208b      208b
```

 

> Создайте snapshot состояния кластера elasticsearch.

Сделать снапшот всего кластера

**#curl -XPUT 'localhost:9200/_snapshot/netology_backup/snapshot_1?wait_for_completion=true'**

 

Приведите в ответе список файлов в директории со snapshot-ами.

```
index-0 

ndex.latest

indices

meta-POhiHc8NR6OODfGYuG10OQ.dat

snap-POhiHc8NR6OODfGYuG10OQ.dat
```

 

> Удалите индекс test и создайте индекс test-2. 

**#curl -XDELETE 'localhost:9200/test'**

 

**#curl -XPUT 'localhost:9200/test-2' -H 'content-type: application/json' -d '{"settings": {"index": {"number_of_shards": 1,"number_of_replicas": 0}}}'**

 

 

 

> Приведите в ответе список индексов.

**#curl 'localhost:9200/_cat/indices?v'**

```
health status index uuid          pri rep docs.count docs.deleted store.size pri.store.size

green open  test-2 qXPeoYMGRdqIZXVexprbDA  1  0     0      0    208b      208b
```

 

 

 

Восстановите состояние кластера elasticsearch из snapshot, созданного ранее.

Приведите в ответе запрос к API восстановления и итоговый список индексов.

 

Так как нужно восстановить состояние кластера, то добавил параметр include_global_state=true

**#curl -XPOST 'localhost:9200/_snapshot/netology_backup/snapshot_1/_restore' -H 'content-type: application/json' -d '{"include_global_state": true}'**

 

 

 

**# curl 'localhost:9200/_cat/indices?v'**

```
health status index uuid          pri rep docs.count docs.deleted store.size pri.store.size

green open  test-2 cxmsCagyT465GxthN8dqvw  1  0     0      0    208b      208b

green open  test  2xUeorqvQVSLY9NwjFDTFA  1  0     0      0    208b      208b
```



Не уверен нужно было ли в последнем задании перед восстановлением удалять все индексы, чтобы состояние после восстановления соответствовало состоянию на момент снимка.



 




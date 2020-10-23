> # Задача 1
>
> Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.
>
> Подключитесь к БД PostgreSQL используя `psql`.
>
> Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.
>
> **Найдите и приведите** управляющие команды для:
> - вывода списка БД
> - подключения к БД
> - вывода списка таблиц
> - вывода описания содержимого таблиц
> - выхода из psql
>



> вывод списка БД

**postgres=# \l**

 

> подключения к БД

\c[onnect] {[DBNAME|- USER|- HOST|- PORT|-] | conninfo}

**postgres=# \c postgres postgres localhost 5432**

 

> вывод списка таблиц

**postgres=# \dt**

 

> вывода описания содержимого таблиц

 \d[S+] NAME      describe table, view, sequence, or index

 **postgres=# \d TABLE_NAME**

 

> выхода из psql

 **\q**





> # Задача 2
>
> Используя `psql` создайте БД `test_database`.
>
> Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).
>
> Восстановите бэкап БД в `test_database`.
>
> Перейдите в управляющую консоль `psql` внутри контейнера.
>
> Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.
>
> Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats) столбец таблицы `orders` 
> с наибольшим средним значением размера элементов в байтах.
>
> **Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.



> Восстановите бэкап БД в test_database.

**\#cat /database/dump/test_dump.sql | psql -h localhost -U postgres test_database**

 

​              

> Подключитесь к восстановленной БД

**postgres=# \c test_database**



> Проведите операцию ANALYZE для сбора статистики по таблице.

**test_database=# ANALYZE orders;**



> Приведите в ответе команду, которую вы использовали для вычисления и полученный результат.

**test_database=# select max(avg_width) from pg_stats where tablename='orders';**

avg_width

\-----------

 16



> # Задача 3
>
> Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
> поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
> провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).
>
> Предложите SQL-транзакцию для проведения данной операции.
>
> Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?



Так как индексы и ограничения не наследуются, то пропишем primary  key

**CREATE TABLE orders_1 (** 

​    **CHECK ( price>499 ),**

​    **CONSTRAINT orders_pkey_1 PRIMARY KEY (id)**

**) INHERITS (orders);**

****



**CREATE TABLE orders_2 (** 

​    **CHECK ( price<=499 ),**

​    **CONSTRAINT orders_pkey_2 PRIMARY KEY (id)**

**) INHERITS (orders);**

****



**INSERT INTO orders_1 SELECT * FROM orders WHERE price > 499;**

**DELETE FROM ONLY orders WHERE price > 499;**

****



**INSERT INTO orders_2 SELECT * FROM orders WHERE price <= 499;**

**DELETE FROM ONLY orders WHERE price <= 499;**

 

Выполнение ONLY тут физически не играет роли, так как не прописаны RULE, но оставил для порядка.

Вместо DELETE в нашем случае можно было воспользоваться TRUNCATE:

**TRUNCATE orders;**



> Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?



Да, до наполнения таблицы нужно было прописать RULE:

Как минимум для вставки данных:

**CREATE RULE orders_insert_to_1 AS ON INSERT TO orders**

**WHERE ( price > 499)**

**DO INSTEAD INSERT INTO orders_1 VALUES (NEW.*);**

****

**CREATE RULE orders_insert_to_2 AS ON INSERT TO orders**

**WHERE ( price <= 499)**

**DO INSTEAD INSERT INTO orders_2 VALUES (NEW.*);**



А также для обновления и удаления:

**CREATE RULE orders_update_to_1 AS ON UPDATE TO orders**

**WHERE ( NEW.price > 499)**

**DO INSTEAD UPDATE orders_1**

​    **SET id = NEW.id,**

​        **title = NEW.title,**

​        **price = NEW.price**

​    **WHERE id = OLD.id;**

****

**CREATE RULE orders_update_to_2 AS ON UPDATE TO orders**

**WHERE ( NEW.price <= 499)**

**DO INSTEAD UPDATE orders_2**

​    **SET id = NEW.id,**

​        **title = NEW.title,**

​        **price = NEW.price**

​    **WHERE id = OLD.id;**

****

**CREATE RULE orders_del_to_1 AS ON DELETE TO orders**

**WHERE ( NEW.price > 499)**

**DO INSTEAD DELETE FROM orders_1**

**WHERE id = OLD.id;**

****

**CREATE RULE orders_del_to_2 AS ON DELETE TO orders**

**WHERE ( NEW.price <= 499)**

**DO INSTEAD DELETE FROM orders_2**

**WHERE id = OLD.id;**

 



> # Задача 4
>
> Используя утилиту `pg_dump` создайте бекап БД `test_database`.
>
> Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?



**#pg_dump -h localhost -U postgres -F p -f 20201023_test_database test_database**

 

Нужно добавить в текст дампа, где ппрописано создание таблицы, ограничение уникальности для столбца title, аналогично для таблиц-шардов

**CREATE TABLE public.orders (**

  **id integer NOT NULL,**

  **title character varying(80) UNIQUE NOT NULL,**

  **price integer DEFAULT 0**

**);**


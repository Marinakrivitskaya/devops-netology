#  Домашнее задание к занятию "6.2. SQL"

## Задача 1

> Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, в который будут складываться данные БД и бэкапы.
>
> Приведите получившуюся команду или docker-compose манифест.

 

 

**/root/docker/postgres-compose/docker-compose.yml:**

*version: "3.3"*

 

*services:*

 *server-postgres:*

  *image: postgres:12.4*

  *#Переменные, необходимые для настройки пользователя, БД*  *postgres*

  *#environment:*

   *# POSTGRES_USER: postgres*

   *# POSTGRES_PASSWORD: 111*

   *# Создать* *БД*

   *# POSTGRES_DB: my_db*

 

  *#Создание volume*

  *volumes:*

​    *- "./database:/database"*

​    *- "./db_backup:/db_backup"*

 

   *#Проброс порта Postgres*

  *ports:*

   *- "5432:5432"*

 

Сборка проекта

**#docker-compose build**

 

 

Запуск проекта

**#****docker-****compose** **up -d**

 

Просмотр, что создались директории для volume

**# docker-compose exec server-postgres ls /**

*bin    dev             home  mnt  run  tmp*

*boot    docker-entrypoint-initdb.d lib  opt  sbin usr*

***database\***  *docker-entrypoint.sh    lib64 proc srv  var*

***db_backup\***  *etc             media root sys*

 





## Задача 2

> В БД из задачи 1:
>
> - создайте     пользователя test-admin-user и БД test-db
> - в     БД test-db создайте таблицу orders и clients (спeцификация таблиц ниже)
> - предоставьте     привилегии на все операции пользователю test-admin-user на таблицы БД     test-db
> - создайте     пользователя test-simple-user
> - предоставьте     пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных     таблиц БД test-db
>
> Таблица orders:
>
> - id     (serial primary key)
> - наименование     (string)
> - цена     (integer)
>
> Таблица clients:
>
> - id     (serial primary key)
> - фамилия     (string)
> - страна     проживания (string, index)
> - заказ     (foreign key orders)
>
> Приведите:
>
> - итоговый     список БД после выполнения пунктов выше,
> - описание     таблиц (describe)
> - SQL-запрос     для выдачи списка пользователей с правами над таблицами test_db
> - список     пользователей с правами над таблицами test_db

 

 

 

Проверяем статус postgres

**# docker-compose exec -u postgres server-postgres pg_ctl status**

*pg_ctl: server is running (PID: 1)*

*/usr/lib/postgresql/12/bin/postgres*

 

**>создайте пользователя** **test****-****admin****-****user** **и БД** **test****-****db**

Подключаемся к postgres

**#****docker-compose exec -u postgres server-postgres psql**

 

Создаем БД test-db , пришлось добавить кавычки из-за присутствия дефиса в именовании

postgres=#**CREATE DATABASE "test-db";**

 

Создаем пользователя test-admin-user

postgres=**#CREATE USER "test-admin-user" WITH PASSWORD '111';**

*CREATE ROLE*

 

**>****в** **БД** **test-db** **создайте** **таблицу** **orders** **и** **clients (****спецификация** **таблиц** **ниже****)**

Переключаемся на созданную БД

**postgres=# postgres=# \c "test-db"**

*You are now connected to database "test-db" as user "postgres".*

Создаем таблицу orders

**test-db=#**

**CREATE TABLE orders(**

**id integer PRIMARY KEY,**

**"наименование" text,**

**"цена" integer**

**);**



Создаем таблицу clients

**CREATE TABLE clients(**

**id integer PRIMARY KEY,**

**"фамилия"** **text****,**

**"****страна** **проживания****" text,**

**"заказ" integer REFERENCES orders(id)**

**);**



Создание индекса

**#CREATE INDEX idx_clients_country ON clients USING btree ("****страна** **проживания****");**

 

 

**>предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test-db**

test-db=# **GRANT ALL ON TABLE clients TO "test-admin-user";**

test-db=# **GRANT ALL ON TABLE orders TO "test-admin-user";**



**>создайте пользователя test-simple-user**

test-db=#**CREATE USER "test-simple-user" WITH PASSWORD '111';**

 

**>предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test-db**

test-db=#GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE clients TO "test-simple-user";

test-db=#GRANT INSERT, SELECT, UPDATE, DELETE ON TABLE orders TO "test-simple-user";





**>итоговый список БД после выполнения пунктов выше,**

**test-db=# \list**

http://prntscr.com/uz45mf



**>описание** **таблиц** **(describe)**

**test-db=# \d orders;**

**test-db=# \d clients;**

http://prntscr.com/uz5lfl

http://prntscr.com/uz65e0

 

**>SQL-запрос для выдачи списка пользователей с правами над таблицами test_db**

**>список пользователей с правами над таблицами test_db**

**SELECT grantee, table_name,privilege_type**

**FROM information_schema.table_privileges**

**WHERE table_catalog='test-db' AND table_schema = 'public'**

**ORDER BY grantee;**

http://prntscr.com/uz4t2b









## Задача 3

> Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:
>
> Таблица orders
>
> | **Наименование** | **цена** |
> | ---------------- | -------- |
> | Шоколад          | 10       |
> | Принтер          | 3000     |
> | Книга            | 500      |
> | Монитор          | 7000     |
> | Гитара           | 4000     |
>
> Таблица clients
>
> | **ФИО**               | **Страна проживания** |
> | --------------------- | --------------------- |
> | Иванов Иван Иванович  | USA                   |
> | Петров Петр  Петрович | Canada                |
> | Иоганн Себастьян  Бах | Japan                 |
> | Ронни Джеймс Дио      | Russia                |
> | Ritchie  Blackmore    | Russia                |
>
>  

INSERT INTO orders(id,"наименование","цена") VALUES(1,'Шоколад', 10);

INSERT INTO orders(id,"наименование","цена") VALUES (2,'Принтер', 3000);

INSERT INTO orders(id,"наименование","цена") VALUES (3,'Книга', 500);

INSERT INTO orders(id,"наименование","цена") VALUES (4,'Монитор', 7000);

INSERT INTO orders(id,"наименование","цена") VALUES (5,'Гитара', 4000);

 

 

INSERT INTO clients(id,"фамилия","страна проживания") VALUES (1,'Иванов Иван Иванович','USA');

INSERT INTO clients(id,"фамилия","страна проживания") VALUES (2,'Петров Петр Петрович', 'Canada');

INSERT INTO clients(id,"фамилия","страна проживания") VALUES (3,'Иоганн Себастьян Бах', 'Japan');

INSERT INTO clients(id,"фамилия","страна проживания") VALUES (4,'Ронни Джеймс Дио', 'Russia');

INSERT INTO clients(id,"фамилия","страна проживания") VALUES (5,'Ritchie Blackmore', 'Russia');

 

Используя SQL синтаксис - вычислите количество записей в каждой таблице и приведите в ответе запрос и получившийся результат.

**#SELECT count(1) FROM orders;**

*5*

 

**#SELECT count(1) FROM clients;**

*5*  







## Задача 4

> Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.
>
> Используя foreign keys свяжите записи из таблиц, согласно таблице:
>
> | **ФИО**               | **Заказ** |
> | --------------------- | --------- |
> | Иванов Иван Иванович  | Книга     |
> | Петров Петр  Петрович | Монитор   |
> | Иоганн Себастьян  Бах | Гитара    |
>
> Приведите SQL-запросы для выполнения данных операций.

**UPDATE clients SET "заказ" = (SELECT id FROM orders WHERE "наименование"='Книга') WHERE "фамилия"='Иванов Иван Иванович';**

**UPDATE clients SET "заказ" = (SELECT id FROM orders WHERE "наименование"='Монитор') WHERE "фамилия"='Петров Петр Петрович';**

**UPDATE clients SET "заказ" = (SELECT id FROM orders WHERE "наименование"='Гитара') WHERE "фамилия"='Иоганн Себастьян Бах';**

 

>Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.

**SELECT "****фамилия****" FROM clients WHERE "****заказ****" IS NOT NULL**

http://prntscr.com/uz6tnr

 

 

 

 

## Задача 5

> Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 (используя директиву EXPLAIN).
>
> Приведите получившийся результат и объясните что значат полученные значения.

**test-db=# EXPLAIN SELECT "фамилия" FROM clients WHERE "заказ" IS NOT NULL;**

​            *QUERY PLAN*

*--------------------------------------------------------*

 *Seq Scan on clients (cost=0.00..1.02 rows=2 width=32)*

  *Filter: ("заказ" IS NOT NULL)*

*(2* *rows)*

Сканирование таблицы Seq Scan – последовательное, блок за блоком (в других БД, называется Full-scan), в противовес есть например сканирование по индексу (их разновидности).

Чтение 1 строки оценено в 0.
Чтение всех строк в 1.02

Rows=2 — приблизительное количество возвращаемых строк при выполнении операции Seq Scan.

Width=32 — средний размер одной строки в байтах.    

Filter: для каждой считанной  строки проверяется условие ("заказ" IS NOT NULL)

 

Похоже такие данные не правдоподобные из-за неправдивой статистики.

Обновляем статистику по данной таблице: 

**#ANALYZE clients;**

**test-db=# EXPLAIN SELECT "фамилия****" FROM clients WHERE "заказ****" IS NOT NULL;**

​            *QUERY PLAN*

*--------------------------------------------------------*

 *Seq Scan on clients (cost=0.00..1.05 rows=3 width=33)*

  *Filter: ("заказ**" IS NOT NULL)*

*(2 rows)*

 

Можно вывести реальный план:

**test-db=# EXPLAIN(ANALYZE) SELECT "фамилия****" FROM clients WHERE "заказ****" IS NOT NULL;**

​                      *QUERY PLAN*

*--------------------------------------------------------------------------------------------------*

 *Seq Scan on clients (cost=0.00..1.05 rows=3 width=33) (actual time=0.007..0.007 rows=3 loops=1)*

  *Filter: ("заказ**" IS NOT NULL)*

  *Rows Removed by Filter: 2*

 *Planning Time: 0.030 ms*

 *Execution Time: 0.015 ms*

*(5 rows)*



 

 

## Задача 6

> Создайте бэкап БД test-db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).
>
> Остановите контейнер с PostgreSQL (но не удаляйте volumes).
>
> Поднимите новый пустой контейнер с PostgreSQL.
>
> Восстановите БД test-db в новом контейнере.
>
> Приведите список операций, который вы применяли для бэкапа данных и восстановления.

 

root@ubuntu20:~/docker/postgres-compose**# docker-compose exec -u root server-postgres /bin/bash**





Делаем простой бэкап

**#pg_basebackup -h localhost -U postgres  -D /db_backup**

 

Останавливаем проект и запускаем снова

**#docker-compose down**

**#docker-compose up -d**

 

По умолчанию данные располагаются: **PGDATA=/var/lib/pgsql/data**

Убить процесс, чтобы восстановить бэкап не получится, тогда завершится контейнер.

Подумал не зря же мы  делали volume для БД  *- "./**database:/**database"*

На хосте скопировал содержимое одного volume в другой. Из "./db_backup:/db_backup"  в "./database:/database"

 

И поменял 

**/root/docker/postgres-compose/docker-compose.yml:**

*version: "3.3"*

 

*services:*

 *server-postgres:*

  *image: postgres:12.4*

  *#Переменные, необходимые для настройки пользователя, БД*  *postgres*

  *environment:*

   *POSTGRES_USER: postgres*

   *POSTGRES_PASSWORD: 111*

  *#Переменная расположение БД*

  **PGDATA: /database**

   *# Создать* *БД*

   *# POSTGRES_DB: my_db*

 

  *#Создание volume*

  *volumes:*

​    *- "./database:/database"*

​    *- "./db_backup:/db_backup"*

 

   *#Проброс порта Postgres*

  *ports:*

   *- "5432:5432"*

 

Сборка проекта

**#docker-compose build**

 

 

Запуск проекта

**#docker-compose up -d**





 


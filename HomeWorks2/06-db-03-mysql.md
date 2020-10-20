> # Задача 1
>
> Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.
>
> Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-03-mysql/test_data) и 
> восстановитесь из него.
>
> Перейдите в управляющую консоль `mysql` внутри контейнера.
>
> Используя команду `\h` получите список управляющих команд.
>
> Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.
>
> Подключитесь к восстановленной БД и получите список таблиц из этой БД.
>
> **Приведите в ответе** количество записей с `price` > 300.
>
> В следующих заданиях мы будем продолжать работу с данным контейнером.





> Посмотреть статус Mysql

**mysql> \s**
*Server version:     8.0.21 MySQL Community Server – GPL*



> Получите список таблиц из этой БД

**mysql> SHOW TABLES;**

+-------------------+

| Tables_in_test_db |

+-------------------+*

| orders      |

+-------------------+

1 row in set (0.00 sec)





> Приведите в ответе количество записей с price > 300.

**mysql> SELECT \* FROM orders WHERE price > 300;**
+----+----------------+-------+
| id | title     | price |
+----+----------------+-------+
| 2 | My little pony |  500 |
+----+----------------+-------+
1 row in set (0.00 sec)





> # Задача 2
>
> Создайте пользователя test в БД c паролем test-pass, используя:
> - плагин авторизации mysql_native_password
> - срок истечения пароля - 180 дней 
> - количество попыток авторизации - 3 
> - максимальное количество запросов в час - 100
> - аттрибуты пользователя:
>     - Фамилия "Pretty"
>     - Имя "James"
>
> Предоставьте привилегии пользователю `test` на операции SELECT базы `test_db`.
>     
> Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test` и 
> **приведите в ответе к задаче**.



> Создайте пользователя test в БД c паролем test-pass

**CREATE USER 'test'@'%' IDENTIFIED WITH mysql_native_password BY 'test-pass'**

**WITH MAX_QUERIES_PER_HOUR 100**

**PASSWORD EXPIRE INTERVAL 180 DAY**

**FAILED_LOGIN_ATTEMPTS 3**

**ATTRIBUTE '{"fname": "James", "lname": "Pretty "}';**



> **Предоставьте привилегии пользователю test на операции SELECT базы test_db.**

**GRANT SELECT ON test_db.\* TO 'test'@'%';**

Для того, чтоб изменения вступили в силу запустите команду обновления

**FLUSH PRIVILEGES;**



> Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю test и приведите в ответе к задаче.
**SELECT \* FROM INFORMATION_SCHEMA.USER_ATTRIBUTES WHERE USER='test';**
+------+------+-----------------------------------------+\
| USER | HOST | ATTRIBUTE                |\***
+------+------+-----------------------------------------+\
| test | %  | {"fname": "James", "lname": " Pretty "} |\
+------+------+-----------------------------------------+\



> # Задача 3
>
> Установите профилирование `SET profiling = 1`.
> Изучите вывод профилирования команд `SHOW PROFILES;`.
>
> Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.
>
> Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
> - на `MyISAM`
> - на `InnoDB`
>

**SET profiling = 1;**



> Исследуйте, какой engine используется в таблице БД test_db и приведите в ответе.

**SHOW TABLE STATUS FROM test_db LIKE 'orders';**

*..Engine = InnoDB*



> Измените engine и приведите время выполнения и запрос на изменения из профайлера в ответе:
>
> •      на MyISAM
>
> •      на InnoDB

**ALTER TABLE orders ENGINE = MyISAM;**

*Query OK, 5 rows affected (0.02 sec)*

*Records: 5 Duplicates: 0 Warnings: 0*

 

Просмотр доступных профилей, где видно более точное время выполнения

**mysql>** **SHOW** **PROFILES;**

*32 | 0.01948600 | ALTER TABLE orders ENGINE = MyISAM*

 

Просмотр детального профиля

**mysql> SHOW PROFILE FOR QUERY 32;**







> # Задача 4 
>
> Изучите файл `my.cnf` в директории /etc/mysql.
>
> Измените его согласно ТЗ (движок InnoDB):
> - Скорость IO важнее сохранности данных
> - Нужна компрессия таблиц для экономии места на диске
> - Размер буффера с незакомиченными транзакциями 1 Мб
> - Буффер кеширования 30% от ОЗУ
> - Размер файла логов операций 100 Мб
>
> Приведите в ответе измененный файл `my.cnf`.
>



**cat /etc/mysql/my.cnf**

*[mysqld]*

*pid-file    = /var/run/mysqld/mysqld.pid*

*socket     = /var/run/mysqld/mysqld.sock*

*datadir     = /var/lib/mysql*

*secure-file-priv= NULL*

 

*#Скорость* *IO важнее сохранности данных*

*innodb_flush_log_at_trx_commit = 2*

 

*#работает быстрее (меньше надежности)*

*innodb_flush_method = O_DIRECT*

 

*#Компрессии таблиц для экономии места на диске*

*innodb_file_per_table = ON*



*#Размер буффера с незакомиченными транзакциями 1 Мб*

*innodb_log_buffer_size = 1M*



 *#Буффер кеширования 30% от ОЗУ*

*innodb_buffer_pool_size = 2G*



*#Размер файла логов операций 100 Мб*

*innodb_log_file_size = 100M*

  

*# Custom config should go here*

*!includedir /etc/mysql/conf.d/*








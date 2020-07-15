# devops-netology
Andrey Krylov
12/07/2020



>1.Найдите полный хеш и комментарий коммита, хеш которого начинается на `aefea`.
Данное начало Hash однозначно определяет коммит, поэтому достаточно команды:
#git show aefea
Имя commit: aefead2207ef7e2aa5dc81a34aedf0cad4c32545
Комментарий: Update CHANGELOG.md



>2.Какому тегу соответствует коммит `85024d3`?
Можно воспользоваться командой для вывода информации о коммите и найти имя тега:
#git show 85024d3
v0.12.23

Или вызвать команду git describe, добавил параметр --tags, так как без него выводятся только annotated tags, на случай если там будет легковесный. Так как пути не будет до тега, то покажет только  имя самого тега.
#git describe --tags 85024d3
v0.12.23



>3.Сколько родителей у коммита `b8d720`? Напишите их хеши.
Первой командой выведем второго родителя, если вернется ошибка, то у коммита 1 родитель, в противном случае получим информацию о коммите второго родителя. 
#git show b8d720^2
Или для дальнейшего сокращения вывод (только хеш):
#git show b8d720^2 --pretty=format:%H --no-patch

Коммит второго родителя: commit 9ea88f22fc6269854151c571162c5bcf958bee2b
#git show --pretty=format:%H b8d720^1
Коммит первого родителя: commit 56cd7859e05c36c06b56d013b55a252d0bb7e158



>4.Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами  v0.12.23 и v0.12.24.
Здесь я сразу понятно, что коммит v0.12.24 идет после v0.12.23 (по порядковому номеру).
При задании диапазона установил последним коммитом предыдущий от v0.12.24 (чтобы он не включался в вывод).
#git log v0.12.23..v0.12.24^



>5.Найдите коммит в котором была создана функция `func providerSource`, ее определение в коде выглядит так `func providerSource(...)` (вместо троеточего перечислены аргументы).

Выполнил команду по поиску изменений в коммитах:
#git log -S 'func providerSource('
Найден commit 8c928e83589d90a031f811fae52a81be7153e82f

или вывести только хеш коммита: 
git log -S 'func providerSource(' --pretty=format:%H
8c928e83589d90a031f811fae52a81be7153e82f



>6.Найдите все коммиты в которых была изменена функция `globalPluginDirs`.
Для полного вывода:
#git log -S ' globalPluginDirs'

Или более удобный, короткий.
#git log -S ' globalPluginDirs'  --oneline
35a058fb3 main: configure credentials from the CLI config file
c0b176109 prevent log output during init
8364383c3 Push plugin discovery down into command package  

Или вывести только полные хеш коммитов: 
#git log -S ' globalPluginDirs'  --pretty=format:%H
35a058fb3ddfae9cfee0b3893822c9a95b920f4c
c0b17610965450a89598da491ce9b6b5cbd6393f
8364383c359a6b738a436d1b7745ccdce178df47



>7. Кто автор функции `synchronizedWriters`?
git log -S'synchronizedWriters'  ищет  коммиты содержащие 'synchronizedWriters', 
а --pretty=format:%an добавлен, чтобы вывести только имя автора.
#git log -S'synchronizedWriters' --pretty=format:%an
Автор: Martin Atkins



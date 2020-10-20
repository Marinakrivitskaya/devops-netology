# -*- coding: utf8 -*-

print ("Введите числа разделенные пробелом")

# Создаем множество
user_set = set ()
user_set2 = set ()

# Создаем список из вводимых чисел
s = [int (i) for i in input ().split ()]

# Проходим по списку.
for i in s:
    # Если число новое то добавляем в множество
    if i not in user_set:
        user_set.add (i)
    # Если число повторяется то добавляем во второе множество
    else:
        user_set2.add (i)

# разбиваем элементы множества и выводим их через пробел
print (" !".join (map (str, user_set2)))

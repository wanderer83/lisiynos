# -*- coding: utf-8 -*-
import sys

sys.path.append('../common')

from gen import go, GenerateIndex, Theme

# Все темы в порядке их следования в курсе
for fn in [
    Theme('', 'Понедельник - 7'),
    ("bits.html", 5, 2, 1, 2),

    Theme('', 'Вторник - 6'),
    ("bits.html", 3, 3, 1, 3),

    Theme('', 'Среда - 6'),
    ("dsu.html", 3, 3, 1, 1), # Деревья и графы. Система непересекающихся множеств. Поиск наименьшего общего предка

    Theme('', "Четверг - 6"),
    ("strings.html", 4, 2, 1, 3),

    Theme('', "Пятница - 7"),
    ("geom.html", 3, 4, 0, 1),

    Theme("Олимпиада", "Суббота - 4"),
    ("../s6/olymp.html", 0, 4, 0, 4), # Командная работа (решение олимпиад прошлых лет)
]:
    go(fn)

GenerateIndex("Сессия 3 - осень (ноябрь): учебно-тематический план")
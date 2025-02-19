Тухватуллина Амина Тестовое задание Системный Аналитик Совкомбанк
Задание 1
Цель: Найти ошибки в данных.
Ход решения

Для решения задачи по выявлению ошибок в данных о выдаче кредитов, представленных в Excel-файле с тремя листами ("выдачи", "продукты" и "точки"), был разработан скрипт на Python с использованием библиотеки Pandas. Целью скрипта является обнаружение ошибок трех уровней: простых ошибок в данных, ошибок в ссылках и логических ошибок.

Для начала реализуем логику ошибок 1 уровня: 
Пишем проверку на то, чтобы дата выдачи кредита не превышала текущую дату (установлена с помощью модуля datetime), если такие записи существуют, это указывает на ошибку. Затем прописываем что суммы выдачи кредитов не являются отрицательными. Отрицательная сумма может свидетельствовать о неверном вводе данных. Помимо проверки на будущие даты и отрицательные суммы выдачи, в коде также проверяются отрицательные суммы страховки и комиссии

Переходим к описанию логики ошибок 2 уровня (ошибки в ссылках)
В предоставленных данных между таблицами установлены следующие связи через идентификаторы (ID):
Связь между таблицами "выдачи" и "продукты" через ID_Продукта:
Описание связи: Каждая запись в таблице "выдачи" содержит поле ID_Продукта, которое указывает на конкретный продукт, связанный с данной выдачей кредита. Это поле является внешним ключом, ссылающимся на первичный ключ ID_Продукта в таблице "продукты". Тип связи: "Многие к одному" 
Связь между таблицами "выдачи" и "точки" через ID_Точки:
Описание связи: В таблице "выдачи" поле ID_Точки указывает на точку продаж, где был выдан кредит. Это поле является внешним ключом, ссылающимся на первичный ключ ID_Точки в таблице "точки".
Тип связи: "Многие к одному" 

Каждый ID_Продукта в таблице "выдачи" должен присутствовать в таблице "продукты". Это подтверждает, что все выданные кредиты связаны с существующими продуктами.

Тоже самое с ID_Точки – кредит может быть выдан только в существующей точке

Описание логики ошибок 3 уровня 
Проверим, что сумма, полученная клиентом на руки, соответствует расчету: сумма выдачи минус сумма страховки и комиссии. Несоответствие может указывать на ошибки в расчетах или вводе данных. В коде также есть проверка на дублирующиеся ID_Заявки и проверка на дату погашения, которая не может быть раньше даты выдачи.
 Итоговый результат:

 

Задание 2
Цель: Объяснить, почему RR 60-90 -> 90-120 >>100%.
Roll Rate (RR) — это показатель, отражающий процент кредитов, переходящих из одной категории просрочки в следующую в течение определенного периода времени.
В нормальной ситуации Roll Rate (RR) ≤ 100%, поскольку основной долг (ОД) не может увеличиваться при переходе между корзинами просрочки. Однако в данных за 30.06.2011 и 31.07.2011 наблюдается, что:
 
Roll Rate (RR) для перехода 60-90 → 90-120 оказался больше 100%, первое, что нужно было проверить — соответствует ли это вообще возможному сценарию. Обычно RR не превышает 100%, потому что основной долг (ОД) может либо уменьшаться (если долги частично погашаются), либо оставаться на том же уровне при полном переходе всех кредитов в следующую корзину. Значит, если RR > 100%, это указывает на аномалию: либо данные содержат дополнительные кредиты, либо произошла ошибка в расчетах.
Дальше нужно было разобраться, действительно ли кредиты из 60-90 перетекли в 90-120, или в корзине 90-120 появились "новые" кредиты, которых раньше в 60-90 не было. Мы взяли данные за 30.06.2011 и 31.07.2011, чтобы сравнить, какие договоры находились в корзине 60-90 на первой дате и какие в 90-120 на второй. Оказалось, что все кредиты, которые были в 60-90, действительно оказались в 90-120, но в этой корзине появилось два дополнительных договора, которых не было в 60-90. Это и стало ключевым моментом: значит, часть долга в корзине 90-120 не пришла из 60-90, а была добавлена из другого источника.
Чтобы понять, откуда взялись эти два дополнительных договора, мы проверили, где они находились 30.06.2011. Оказалось, что они раньше числились в корзине 150-180, а потом "переместились" в 90-120. Это необычная ситуация, потому что логика просрочки предполагает, что кредиты переходят только вперед (например, из 60-90 в 90-120), но здесь кредиты как будто "откатились назад".
Такая переклассификация может происходить по нескольким причинам. Возможно, по этим договорам была реструктуризация, и их статус изменился – например, часть долга была погашена, и теперь они считаются менее проблемными, чем раньше. Другая возможность — изменение правил учета или корректировка данных, из-за чего они оказались в другой корзине.
Теперь становится понятно, почему RR оказался больше 100%. Формально мы считали RR как (ОД в 90-120 на 31.07) / (ОД в 60-90 на 30.06), но в числителе оказалось больше долгов, чем перетекло из 60-90, потому что добавились еще эти два "новых" кредита. Если бы мы считали RR только для тех договоров, которые действительно перешли из 60-90, он был бы ровно 100%, что соответствует нормальной ситуации.
Таким образом, аномально высокий RR объясняется не ошибками в данных, а тем, что в корзину 90-120 попали не только кредиты из 60-90, но и дополнительные кредиты, "вернувшиеся" из 150-180. Это показывает, как важно не просто механически рассчитывать показатели, но и проверять, какие именно кредиты участвуют в этих переходах, чтобы правильно интерпретировать данные.
Задание 3
Цель: Посчитайть примерно, сколько банк может заработать за год.

Формула для расчета суммы, которую банк должен выплатить вкладчику через год:
S=P*(1+r)
S — итоговая сумма депозита,
P— 120 000 начальная сумма депозита,
r — 0,1 годовая процентная ставка (в десятичной форме).
S=120 000*(1+0,1)=132 000
Cпособ расчета номинальной месячной процентной ставки, если в задаче проценты начисляются ежемесячно, но ставка дана годовая.
r_мес=r_год/12*100=  0,10/12*100=0,83%

Начальная сумма 120 000 руб. каждый месяц выдаётся в кредит, и благодаря ежемесячному возврату с процентами банк может реинвестировать полученные деньги. Итоговая сумма через 12 месяцев при ежемесячном компаундировании будет
120 000*(1+r)^12=120 000*〖(1+0,1/12)〗^12
В то же время банк должен через год выплатить вкладчику депозит с начислением 10% годовых, то есть 132 000
Таким образом, прибыль банка – это разница между суммой, полученной по кредитам, и суммой, которую нужно выплатить:
Прибыль=120 000*[(1+ 〖0,1/12〗^12 )-1.1]≈565,57руб


Прибыль банка 565,57
Задание 4
Цель: Дать правильный ответ к задачке.
Так как в ящике с надписью «Цветы» не могут быть цветы, он обязан содержать единственный оставшийся вариант — огурцы.
Ящик с надписью «Ромашки» не может содержать ромашки, значит, там должны быть колокольчики.
Ящик с надписью «Огурцы» тогда получит оставшиеся ромашки.

Ответ: В ящике с надписью "Ромашки" вырастут колокольчики.


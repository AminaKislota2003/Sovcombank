import pandas as pd
from datetime import datetime

# Загрузка данных из Excel
file_path = 'data.xlsx'
sheets = pd.read_excel(file_path, sheet_name=None)

# Получение данных из листов
df_issuances = sheets['выдачи']
df_products = sheets['продукты']
df_points = sheets['точки ']

# 1-й уровень: Простые ошибки в данных
print("1-й уровень: Простые ошибки в данных")

# Проверка на будущие даты выдачи кредита
future_dates = df_issuances[df_issuances['Дата выдачи'] > datetime.now()]
if not future_dates.empty:
    print("Найдены записи с будущей датой выдачи кредита:")
    print(future_dates[['ID_Заявки', 'Дата выдачи']])
else:
    print("Ошибок с будущими датами выдачи не найдено.")

# Проверка на отрицательные суммы выдачи
negative_amounts = df_issuances[df_issuances['Сумма выдачи'] < 0]
if not negative_amounts.empty:
    print("Найдены записи с отрицательной суммой выдачи:")
    print(negative_amounts[['ID_Заявки', 'Сумма выдачи']])
else:
    print("Ошибок с отрицательными суммами выдачи не найдено.")

# Проверка на отрицательные суммы страховки и комиссии
negative_fees = df_issuances[(df_issuances['Сумма Страховки'] < 0) | (df_issuances['Сумма Комиссии'] < 0)]
if not negative_fees.empty:
    print("Найдены записи с отрицательными значениями в страховке или комиссии:")
    print(negative_fees[['ID_Заявки', 'Сумма Страховки', 'Сумма Комиссии']])
else:
    print("Ошибок с отрицательными суммами страховки и комиссии не найдено.")

# 2-й уровень: Ошибки в ссылках
print("\n2-й уровень: Ошибки в ссылках")

# Проверка на существование ID_Продукта в справочнике продуктов
invalid_products = df_issuances[~df_issuances['ID_Продукта'].isin(df_products['ID_Продукта'])]
if not invalid_products.empty:
    print("Найдены записи с несуществующими ID_Продукта:")
    print(invalid_products[['ID_Заявки', 'ID_Продукта']])
else:
    print("Ошибок с некорректными ID_Продукта не найдено.")

# Проверка на существование ID_Точки в справочнике точек
invalid_points = df_issuances[~df_issuances['ID_Точки'].isin(df_points['ID_Точки'])]
if not invalid_points.empty:
    print("Найдены записи с несуществующими ID_Точки:")
    print(invalid_points[['ID_Заявки', 'ID_Точки']])
else:
    print("Ошибок с некорректными ID_Точки не найдено.")

# Проверка на дубликаты по ID_Заявки
duplicate_requests = df_issuances[df_issuances.duplicated(subset=['ID_Заявки'], keep=False)]
if not duplicate_requests.empty:
    print("Найдены дубликаты ID_Заявки:")
    print(duplicate_requests[['ID_Заявки']])
else:
    print("Ошибок с дублирующимися ID_Заявки не найдено.")

# 3-й уровень: Логические ошибки
print("\n3-й уровень: Логические ошибки")

# Заполняем NaN нулями в колонках "Сумма Страховки" и "Сумма Комиссии"
df_issuances[['Сумма Страховки', 'Сумма Комиссии']] = df_issuances[['Сумма Страховки', 'Сумма Комиссии']].fillna(0)

# Проверка на соответствие суммы на руки и суммы выдачи за вычетом страховки и комиссии
df_issuances['Рассчитанная сумма на руки'] = df_issuances['Сумма выдачи'] - df_issuances['Сумма Страховки'] - df_issuances['Сумма Комиссии']

df_issuances['Сумма на руки'] = df_issuances['Сумма на руки'].round(2)
df_issuances['Рассчитанная сумма на руки'] = df_issuances['Рассчитанная сумма на руки'].round(2)

mismatch_amounts = df_issuances[df_issuances['Сумма на руки'] != df_issuances['Рассчитанная сумма на руки']]
if not mismatch_amounts.empty:
    print("Найдены записи с несоответствием суммы на руки и рассчитанной суммы:")
    print(mismatch_amounts[['ID_Заявки', 'Сумма на руки', 'Сумма выдачи', 'Сумма Страховки', 'Сумма Комиссии', 'Рассчитанная сумма на руки']])
else:
    print("Логических ошибок в суммах не найдено.")

# Проверка на дату погашения раньше даты выдачи
if 'Дата погашения' in df_issuances.columns:
    invalid_dates = df_issuances[df_issuances['Дата погашения'] < df_issuances['Дата выдачи']]
    if not invalid_dates.empty:
        print("Найдены записи, где дата погашения раньше даты выдачи:")
        print(invalid_dates[['ID_Заявки', 'Дата выдачи', 'Дата погашения']])
    else:
        print("Ошибок с датами погашения не найдено.")



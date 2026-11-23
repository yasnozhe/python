import pandas as pd
import numpy as np

from data import data
df_base = pd.DataFrame(data)

print("Задача 1")
series_data = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print("1.1 Series:\n", series_data)
print("\n1.2 DataFrame из словаря:")
df1 = df_base.copy()
print(df1)
print("\n1.3 Первые 3 строки (.head):")
print(df1.head(3))
print("\n1.3 Последние 3 строки (.tail):")
print(df1.tail(3))
print("\n1.3 Информация о типах (.info):")
df1.info()
print("\n1.3 Статистика (.describe):")
print(df1.describe())


print("Задача 2")
df2 = df_base.copy()
print("2.1 Имя и зарплата для IT:")
print(df2[df2['department'] == 'IT'][['name', 'salary']])
print("\n2.2 Первые 3 строки и 2 столбца (iloc):")
print(df2.iloc[:3, :2])
print("\n2.3 Зарплата > 70000:")
print(df2[df2['salary'] > 70000])
df2['total_comp'] = df2['salary'] + df2['bonus'].fillna(0)
print("\n2.4 Новый столбец total_comp:")
print(df2[['name', 'salary', 'bonus', 'total_comp']])
df2 = df2.drop(columns=['hire_date'])
print("\n2.5 Столбцы после удаления hire_date:", df2.columns.tolist())


print("Задача 3")
df3 = df_base.copy()
print("3.1 Количество пропусков по столбцам:")
print(df3.isna().sum())
df3['salary'] = df3.groupby('department')['salary'].transform(lambda x: x.fillna(x.mean()))
print("\n3.2 Зарплата после заполнения средним по отделу:")
print(df3[['name', 'department', 'salary']])
df3['bonus'] = df3['bonus'].fillna(0)
print("\n3.3 Бонус после заполнения нулями:")
print(df3[['name', 'bonus']])
df3 = df3.dropna(subset=['salary'])
print("\n3.4 Пропуски после очистки:")
print(df3.isna().sum())


print("Задача 4")
df4 = df_base.copy()
print("4.1 Средняя зарплата по отделам:")
print(df4.groupby('department')['salary'].mean())
print("\n4.2 Агрегация по отделам:")
agg_result = df4.groupby('department').agg({
    'salary': 'mean',
    'bonus': 'max',
    'name': 'count'
})
agg_result.columns = ['avg_salary', 'max_bonus', 'emp_count']
print(agg_result)
print("\n4.3 Сводная таблица (pivot_table):")
print(df4.pivot_table(index='department', values='salary', aggfunc='mean'))
print("\n4.4 Отделы по убыванию средней зарплаты:")
avg_salary_sorted = df4.groupby('department')['salary'].mean().sort_values(ascending=False)
print(avg_salary_sorted)


print("Задача 5")
df5 = df_base.copy()
managers_data = {
    'department': ['IT', 'HR', 'Finance'],
    'manager': ['Алексей', 'Екатерина', 'Владимир']
}
df_managers = pd.DataFrame(managers_data)
print("5.1 DataFrame руководителей:")
print(df_managers)
df5 = pd.merge(df5, df_managers, on='department', how='left')
print("\n5.2 DataFrame после merge (left join):")
print(df5[['name', 'department', 'manager']])
new_emp = pd.DataFrame({
    'name': ['Николай'],
    'department': ['IT'],
    'salary': [78000],
    'bonus': [4500],
    'hire_date': pd.to_datetime(['2023-01-10']),
    'manager': ['Алексей']
})
df5 = pd.concat([df5, new_emp], ignore_index=True)
print("\n5.3 Последние строки после добавления Николая (concat):")
print(df5.tail(2))
df5 = df5.reset_index(drop=True)
print("\n5.4 Индекс сброшен, последние индексы:", df5.index[-3:].tolist())


print("Задача 6")
df6 = df3.copy()
df6['total_comp'] = df6['salary'] + df6['bonus']
print("6.1 Топ-3 по total_comp:")
top3 = df6.nlargest(3, 'total_comp')[['name', 'department', 'total_comp']]
print(top3)
print("\n6.2 Средняя зарплата и средний бонус по отделам:")
mean_stats = df6.groupby('department')[['salary', 'bonus']].mean()
print(mean_stats)
df6['is_rich'] = df6['salary'] > 75000
share_rich = df6.groupby('department')['is_rich'].mean()
print("\n6.3 Доля сотрудников с ЗП > 75000 по отделам:")
print(share_rich)
import numpy as np
import time

print("Задача 6.1")
arr = np.arange(20)
print(f"Исходный массив: {arr}")
print("Каждый третий (с индекса 1):", arr[1::3])
print("С 5-го по 14-й в обратном порядке:", arr[5:15][::-1])
print("Последние 5 в обратном порядке:", arr[-5:][::-1])

print("\nЗадача 6.2")
matrix = np.random.randint(0, 10, size=(6, 6))
print("Исходная матрица:\n", matrix)
submatrix = matrix[2:5, 1:4]
print("Подматрица (строки 2-4, столбцы 1-3):\n", submatrix)
diag = np.diagonal(matrix)
print("Главная диагональ:", diag)
rows, cols = np.indices(matrix.shape)
chess_mask = (rows + cols) % 2 == 0
chess_elements = matrix[chess_mask]
print("Элементы с четной суммой индексов:", chess_elements)

print("\nЗадача 6.3")
a = np.array([10, 20, 30, 40, 50, 60])
m = np.arange(12).reshape(3, 4)
print("Массив a:", a)
print("Матрица m:\n", m)
print("1. Элементы a по индексам [0,2,4]:", a[[0, 2, 4]])
rows_idx = [0, 1, 2]
cols_idx = [1, 3, 0]
print("2. Попарные элементы (0,1), (1,3), (2,0):", m[rows_idx, cols_idx])
block = m[np.ix_([0, 2], [1, 3])]
print("3. Блок 2x2:\n", block)

print("\nЗадача 6.4")
x = np.random.randn(1000)
count_gt_1 = np.sum(x > 1)
print("1. Количество элементов > 1:", count_gt_1)
x_modified = x.copy()
x_modified[x_modified < 0] = 0
print("2. Отрицательные заменены на 0 (первые 5 элементов):", x_modified[:5])
x_sign_changes = x.copy()
sign_change_indices = np.where(x[:-1] * x[1:] < 0)[0] + 1
x_sign_changes[sign_change_indices] = 0
print(f"3. Найдено смен знака: {len(sign_change_indices)}. Обнулено.")
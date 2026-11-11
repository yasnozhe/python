import numpy as np

A = np.arange(20).reshape(4, 5)
print("Массив A:\n", A)


row1 = A[1, :]
col3 = A[:, 3]
sub = A[1:4, 2:5]
print("Вторая строка:", row1)
print("Столбец 3:", col3)
print("Подмассив:\n", sub)


rows = [0, 2, 3]
cols = [1, 4]
sub_fancy = A[np.ix_(rows, cols)]
print("Выбранные элементы:\n", sub_fancy)


B = np.array([[-1, 2, -3], [4, -5, 6]])
B[B < 0] = 0
print("После замены отрицательных на 0:\n", B)


B = np.arange(4).reshape(4, 1)
C = np.arange(5).reshape(1, 5)
D = B + C
print("Результат сложения B и C:\n", D)
print("Форма результата:", D.shape)
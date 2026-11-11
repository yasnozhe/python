import numpy as np
from scipy.sparse import random as sparse_random
import timeit


np.random.seed(42)
A_sparse = sparse_random(5, 5, density=0.2, format='csr', random_state=42)
print("4.1 Разреженная матрица 5x5 (CSR):")
print(A_sparse.toarray())
print(f"Количество ненулевых элементов: {A_sparse.nnz}\n")


A_coo = A_sparse.tocoo()
A_csc = A_sparse.tocsc()
print("4.2 Формат COO (координаты и значения):")
print(f"Строки:  {A_coo.row}")
print(f"Столбцы: {A_coo.col}")
print(f"Значения:{A_coo.data}\n")
print("Формат CSC (сжатие по столбцам):")
print(f"Указатели: {A_csc.indptr}")
print(f"Индексы:   {A_csc.indices}")
print(f"Значения:  {A_csc.data}\n")


v_small = np.random.rand(5)
result_small = A_sparse.dot(v_small)
print("4.3 Результат умножения разреженной матрицы на плотный вектор:")
print(result_small, "\n")


n = 1000
density = 0.01
A_sp = sparse_random(n, n, density=density, format='csr', random_state=0)
v = np.random.rand(n)
A_dense = A_sp.toarray()
print("4.4 Замер времени умножения матрицы 1000x1000 на вектор...")
time_sp = timeit.timeit(lambda: A_sp.dot(v), number=10)
time_dense = timeit.timeit(lambda: A_dense.dot(v), number=10)
print(f"Время для РАЗРЕЖЕННОЙ матрицы: {time_sp:.6f} сек.")
print(f"Время для ПЛОТНОЙ матрицы:     {time_dense:.6f} сек.")
print(f"Разреженная матрица быстрее в {time_dense / time_sp:.1f} раз(а)!")
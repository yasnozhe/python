import numpy as np
from scipy.sparse import coo_matrix, csr_matrix, random as sparse_random
import time
import matplotlib.pyplot as plt

print("Задача 8.1")
N = 10000
np.random.seed(42)
rows = np.random.randint(0, 5000, N)
cols = np.random.randint(0, 5000, N)
data = np.random.rand(N)
coo = coo_matrix((data, (rows, cols)), shape=(5000, 5000))
csr = coo.tocsr()
print(f"Количество переданных элементов (с дублями): {N}")
print(f"Количество уникальных ненулевых элементов в CSR (nnz): {csr.nnz}")
print("Это нормально, если nnz меньше 10000, так как совпадающие индексы суммировались.")

print("\nЗадача 8.2")
n = 4000
density = 0.005
vec = np.random.rand(n)
A_sparse = sparse_random(n, n, density=density, format='csr', random_state=42)
A_dense = A_sparse.toarray()
size_dense = A_dense.nbytes / (1024 * 1024)
size_sparse = (A_sparse.data.nbytes + A_sparse.indices.nbytes + A_sparse.indptr.nbytes) / (1024 * 1024)
print(f"Память для Dense: {size_dense:.2f} МБ")
print(f"Память для CSR:   {size_sparse:.2f} МБ")
print(f"Разреженная экономит память в {size_dense / size_sparse:.1f} раз!")
start = time.perf_counter()
_ = A_sparse.dot(vec)
t_sparse = time.perf_counter() - start

start = time.perf_counter()
_ = A_dense.dot(vec)
t_dense = time.perf_counter() - start
print(f"\nВремя умножения CSR:   {t_sparse:.6f} с")
print(f"Время умножения Dense: {t_dense:.6f} с")
print(f"CSR быстрее в {t_dense / t_sparse:.1f} раз!")

print("\nЗадача 8.3")
n = 2000
densities = [0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
times_sparse = []
times_dense = []
x = np.random.rand(n)
print(f"{'Плотность':<12} | {'Sparse (с)':<12} | {'Dense (с)':<12}")
print("-" * 40)
for d in densities:
    A_s = sparse_random(n, n, density=d, format='csr', random_state=42)
    A_d = A_s.toarray()

    t0 = time.perf_counter()
    A_s.dot(x)
    t_s = time.perf_counter() - t0

    t0 = time.perf_counter()
    A_d.dot(x)
    t_d = time.perf_counter() - t0

    times_sparse.append(t_s)
    times_dense.append(t_d)
    print(f"{d:<12.3f} | {t_s:<12.6f} | {t_d:<12.6f}")
plt.figure(figsize=(8, 5))
plt.plot(densities, times_sparse, marker='o', label='Sparse (CSR)', color='blue')
plt.plot(densities, times_dense, marker='s', label='Dense', color='red')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Плотность (доля ненулевых)')
plt.ylabel('Время умножения, с')
plt.title('A @ x: Sparse vs Dense')
plt.grid(True, which="both", ls="--")
plt.legend()
plt.show()
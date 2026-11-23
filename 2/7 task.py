import numpy as np
import os
import time

print("Задача 7.1")
filename = 'big.dat'
shape = (50000, 200)
dtype = np.float32
fp = np.memmap(filename, dtype=dtype, mode='w+', shape=shape)
fp[:] = np.random.rand(*shape)
fp.flush()
expected_size = 50000 * 200 * 4
actual_size = os.path.getsize(filename)
print(f"Ожидаемый размер: {expected_size} байт")
print(f"Фактический размер: {actual_size} байт")
print(f"Размеры совпадают: {expected_size == actual_size}")

print("\nЗадача 7.2")
fp_read = np.memmap(filename, dtype=dtype, mode='r', shape=shape)
global_min = np.inf
global_max = -np.inf
global_sum = 0.0
total_elements = shape[0] * shape[1]
batch_size = 1000
for i in range(0, shape[0], batch_size):
    batch = fp_read[i:i+batch_size, :]
    global_min = min(global_min, np.min(batch))
    global_max = max(global_max, np.max(batch))
    global_sum += np.sum(batch)
global_mean = global_sum / total_elements
print(f"Глобальный MIN: {global_min:.4f}")
print(f"Глобальный MAX: {global_max:.4f}")
print(f"Глобальное среднее: {global_mean:.4f}")

print("\nЗадача 7.3")
N = 3000
arr_c = np.random.rand(N, N)
start = time.perf_counter()
sum_c_rows = 0
for i in range(N):
    for j in range(N):
        sum_c_rows += arr_c[i, j]
time_c_rows = time.perf_counter() - start
start = time.perf_counter()
sum_c_cols = 0
for j in range(N):
    for i in range(N):
        sum_c_cols += arr_c[i, j]
time_c_cols = time.perf_counter() - start
print(f"Массив C-order. Обход по строкам: {time_c_rows:.3f} с")
print(f"Массив C-order. Обход по столбцам: {time_c_cols:.3f} с")
print(f"Обход по столбцам медленнее в {time_c_cols / time_c_rows:.1f} раз(а)")
arr_f = np.asfortranarray(arr_c)
start = time.perf_counter()
sum_f_rows = 0
for i in range(N):
    for j in range(N):
        sum_f_rows += arr_f[i, j]
time_f_rows = time.perf_counter() - start

start = time.perf_counter()
sum_f_cols = 0
for j in range(N):
    for i in range(N):
        sum_f_cols += arr_f[i, j]
time_f_cols = time.perf_counter() - start
print(f"Массив F-order. Обход по строкам: {time_f_rows:.3f} с")
print(f"Массив F-order. Обход по столбцам: {time_f_cols:.3f} с")
print(f"Обход по строкам медленнее в {time_f_rows / time_f_cols:.1f} раз(а)")

print("\nЗадача 7.4")
N = 10_000_000
a = np.random.rand(N)
b = np.random.rand(N)
a_list = a.tolist()
b_list = b.tolist()
res_list = [0.0] * N
start = time.perf_counter()
for i in range(N):
    res_list[i] = (a_list[i] + b_list[i]) / (a_list[i] - b_list[i] + 1)
t_py = time.perf_counter() - start
print(f"1. Python-цикл (list): {t_py:.3f} с")
start = time.perf_counter()
res_np = (a + b) / (a - b + 1)
t_np = time.perf_counter() - start
print(f"2. NumPy в одну строку: {t_np:.3f} с (ускорение x{t_py/t_np:.1f})")
out_arr = np.empty_like(a)
start = time.perf_counter()
num_buf = np.empty_like(a)
den_buf = np.empty_like(a)
np.add(a, b, out=num_buf)       # num = a + b
np.subtract(a, b, out=den_buf)  # den = a - b
np.add(den_buf, 1, out=den_buf) # den = den + 1
np.divide(num_buf, den_buf, out=out_arr) # out = num / den
t_np_out = time.perf_counter() - start
print(f"3. NumPy с out=: {t_np_out:.3f} с")
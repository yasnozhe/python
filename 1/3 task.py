import numpy as np
import os
import timeit


filename = 'large_array.dat'
shape = (1000, 1000)
dtype = np.float64

print("Создаем memory-mapped файл...")
fp = np.memmap(filename, dtype=dtype, mode='w+', shape=shape)
fp[:] = np.random.rand(*shape)
fp.flush()
print(f"Файл {filename} успешно создан. Размер: {os.path.getsize(filename) / (1024*1024):.2f} МБ")


print("\nЧитаем строку и столбец...")

del fp
fp_read = np.memmap(filename, dtype=dtype, mode='r', shape=shape)
row_500 = fp_read[500, :]
col_500 = fp_read[:, 500]
print("Первые 5 элементов 500-й строки:", row_500[:5])
print("Первые 5 элементов 500-го столбца:", col_500[:5])


print("\nСравниваем время обхода...")
def traverse_row_major():
    return sum(fp_read[i, j] for i in range(1000) for j in range(1000))
def traverse_col_major():
    return sum(fp_read[i, j] for j in range(1000) for i in range(1000))

time_row = timeit.timeit(traverse_row_major, number=1)
time_col = timeit.timeit(traverse_col_major, number=1)

print(f"Время обхода по строкам (row-major): {time_row:.4f} сек.")
print(f"Время обхода по столбцам (column-major): {time_col:.4f} сек.")
del fp_read
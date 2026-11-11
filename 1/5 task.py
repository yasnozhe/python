import time
import os
import numpy as np

def sum_sq_py(lst):
    s = 0.0
    for x in lst:
        s += x * x
    return s

N = 10 ** 7
print("Генерация списка из 10^7 элементов...")
data_list = [0.5] * N

t0 = time.perf_counter()
res_py = sum_sq_py(data_list)
t_py = time.perf_counter() - t0
print(f"sum_sq_py(list из {N:,} элементов) = {res_py:.3f}, время = {t_py:.3f} с\n")

print("ЗАДАЧА 5.2 — Cython-версия (.pyx) и компиляция")

pyx_code = """# fastsum.pyx
# cython: language_level=3

def sum_sq_cython(list lst):
    cdef double s = 0.0
    cdef double x
    for x in lst:          # типизированный цикл -> чистый C-код
        s += x * x
    return s
"""

setup_code = """# setup.py
from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("fastsum.pyx"))
"""

workdir = "cython_part"
os.makedirs(workdir, exist_ok=True)

with open(os.path.join(workdir, "fastsum.pyx"), "w", encoding="utf-8") as f:
    f.write(pyx_code)
with open(os.path.join(workdir, "setup.py"), "w", encoding="utf-8") as f:
    f.write(setup_code)
print("Сохранены файлы fastsum.pyx и setup.py в папке", workdir)

cython_ok = False
try:
    from Cython.Build import cythonize
    from setuptools import setup

    cwd = os.getcwd()
    os.chdir(workdir)

    print("Попытка компиляции Cython...")
    setup(script_args=["build_ext", "--inplace"],
          ext_modules=cythonize("fastsum.pyx", quiet=True))

    os.chdir(cwd)
    cython_ok = True
    print("Cython-модуль успешно скомпилирован!")
except Exception as e:
    print(f"\nCython недоступен в этой среде ({e}).")
    print("Скорее всего, на компьютере не установлен компилятор C.")


print("\nЗАДАЧА 5.3 — сравнение времени выполнения (10^7 элементов)")

if cython_ok:
    import sys

    if workdir not in sys.path:
        sys.path.insert(0, workdir)

    import fastsum

    t0 = time.perf_counter()
    res_cy = fastsum.sum_sq_cython(data_list)
    t_cy = time.perf_counter() - t0
    print(f"Cython:  {res_cy:.3f}, время = {t_cy:.3f} с  (ускорение x{t_py / t_cy:.1f})")
else:
    print("Переходим на запасной вариант с NumPy...")
    arr = np.array(data_list)
    t0 = time.perf_counter()
    res_np = float((arr ** 2).sum())
    t_np = time.perf_counter() - t0
    print(f"(среда без Cython) NumPy-версия: {res_np:.3f}, время = {t_np:.3f} с")
    print(f"Векторизованный NumPy быстрее питоновского цикла в ~{t_py / t_np:.0f} раз.")
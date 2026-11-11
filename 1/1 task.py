import numpy as np

a = np.array([0.2, 0.4, 0.6], dtype=np.float32)
sum_a = np.sum(a)
print(f"Сумма float32: {sum_a}")
print(f"Точное значение: {0.2 + 0.4 + 0.6}")
print(f"Разница: {sum_a - (0.2 + 0.4 + 0.6)}")

eps32 = np.finfo(np.float32).eps
eps64 = np.finfo(np.float64).eps
print(f"Машинное эпсилон float32: {eps32}")
print(f"Машинное эпсилон float64: {eps64}")

x = np.float32(1e8)
y = np.float32(1.0)
result = (x + y) - x
print(f"(1e8 + 1) - 1e8 = {result}")
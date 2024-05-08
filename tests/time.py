from decimal import Decimal
from tube import Tube
import time

t_1 = time.perf_counter()
t = Tube(1, 1, 1, Decimal(0.05))
t_2 = time.perf_counter()
print("Инстанцирование и разбиение:", t_2 - t_1, "s")

t_1 = time.perf_counter()
coeffs = t.calc_angular_coeffs()
t_2 = time.perf_counter()
print("Расчет коэффициентов:", t_2 - t_1, "s")

t_1 = time.perf_counter()
ans = t.solve_sle(coeffs)
t_2 = time.perf_counter()
print("Решение СЛУ:", t_2 - t_1, "s")

t_1 = time.perf_counter()
k = t.calc_clausing(coeffs)
t_2 = time.perf_counter()
print("Расчет КК:", t_2 - t_1, "s")

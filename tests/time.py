from sep.round import RoundSeparator
from decimal import Decimal
from tube import Tube
import time

t_1 = time.perf_counter()
s = RoundSeparator(10, 20, 10000)
k = s.calc_clausing(s.calc_ac())
t_2 = time.perf_counter()
print(f"Расчет КК(время с начала запуска при n={s._count_cells}):", t_2 - t_1, "s")

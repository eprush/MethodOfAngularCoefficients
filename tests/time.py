from separator.round import RoundSeparator
from matplotlib import pyplot as plt
import timeit


def time_test(L, n) -> float:
    s = RoundSeparator(0.5, L, n)
    return s.calc_clausing(s.calc_ac())


if __name__ == "__main__":
    how_many_times = 10
    nums = list(range(1, 1000, 10))
    times = [0.0] * len(nums)
    for i in range(len(nums)):
        sum_time = timeit.timeit(f"time_test(900, {nums[i]})",
                                 number=how_many_times, setup="from __main__ import time_test")
        times[i] = sum_time / how_many_times
        print(i)
    plt.plot(nums, times)
    plt.xlabel("Количество колец n", size=17)
    plt.ylabel("Время расчета КК, с", size=17)
    plt.title("Временная сложность", size=18)
    plt.grid()
    plt.show()

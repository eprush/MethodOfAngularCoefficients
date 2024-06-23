from memory_profiler import profile
from separator.round import RoundSeparator
from matplotlib import pyplot as plt
from numpy import array


@profile
def space_test(L, n) -> float:
    s = RoundSeparator(0.5, L, n)
    coeffs = s.calc_ac()
    return s.calc_clausing(coeffs)


if __name__ == "__main__":
    space_test(900, 1000)

    mem_usage = [0.1, 1.1, 1.3, 1.8, 2.2, 2.5, 2.8, 3.1, 4.2, 5.0, 4.4, 4.3, 5.0, 5.0, 6.0, 6.9, 6.3, 6.9, 6.8,
                 6.9, 6.9]
    mem_usage = array(mem_usage)/2**20*10**6
    nums = [1] + list(range(50, 1050, 50))
    plt.plot(nums, mem_usage)
    plt.xlabel("Количество колец n", size=17)
    plt.ylabel("Затраченная память, Мб", size=17)
    plt.title("Пространственная сложность", size=18)
    plt.grid()
    plt.show()

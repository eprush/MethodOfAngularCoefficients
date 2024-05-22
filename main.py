import numpy as np
from separator.round import RoundSeparator
from matplotlib import pyplot as plt
from numpy.typing import NDArray
from graphs import experimental_cc


def plot_num_of_cells(R, L, nums: NDArray[int]):
    def calc_graph():
        Y = np.zeros(len(nums), dtype=float)
        for i in range(len(nums)):
            s = RoundSeparator(R, L, nums[i])
            coeffs = s.calc_ac()
            Y[i] = s.calc_clausing(coeffs)
        return Y

    plt.xlabel("Количество ячеек n", size=17)
    plt.ylabel("Коэффициент Клаузинга", size=17)
    plt.plot(nums, calc_graph())
    plt.grid()
    plt.show()
    return


def plot_len(R, lens, nums, k: NDArray = None):
    def calc_graph(n):
        Y = np.zeros(len(lens), dtype=float)
        for i in range(len(lens)):
            s = RoundSeparator(R, lens[i], n)
            coeffs = s.calc_ac()
            Y[i] = s.calc_clausing(coeffs)
        return Y

    def clausing():
        for num in nums:
            plt.plot(lens, graphs[num], label=f"{num}")
        if k is not None and len(k):
            plt.plot(lens, k, label=f"эксперимент")
        plt.xlabel("Длина канала L/R", size=17)
        plt.ylabel("Коэффициент Клаузинга", size=17)
        plt.legend(title="Количество колец")
        plt.grid()
        plt.show()
        return

    def deviation_clausing():
        if k is None or not len(k):
            raise ValueError("Invalid value of the k parameter at the plot_deviation_len function")
        for num in nums:
            plt.plot(lens, (graphs[num] - k) / k * 100, label=f"{num}")
        plt.xlabel("Длина канала L/R", size=17)
        plt.ylabel("Отклонение КК, %", size=17)
        plt.legend(title="Количество колец")
        plt.grid()
        plt.show()
        return

    graphs = {num: calc_graph(num) for num in nums}
    clausing()
    deviation_clausing()
    return


plot_num_of_cells(1, 2, np.arange(1, 31))
plot_len(0.5, list(experimental_cc.keys()), np.arange(1, 11, 3), list(experimental_cc.values()))

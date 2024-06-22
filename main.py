import numpy as np
from matplotlib import pyplot as plt
from numpy.typing import NDArray
from MNK import Interpolator
from math import isclose
from separator.round import RoundSeparator
from theoretical_cc import theoretical_cc


def plot_num_of_cells(R, L, nums: NDArray[int]):
    def calc_num_graph():
        Y = np.zeros(len(nums), dtype=float)
        for i in range(len(nums)):
            s = RoundSeparator(R, L, nums[i])
            coeffs = s.calc_ac()
            Y[i] = s.calc_clausing(coeffs)
        print(Y[-1])
        return Y

    plt.xlabel("Количество ячеек n", size=17)
    plt.ylabel("Коэффициент Клаузинга", size=17)
    plt.plot(nums, calc_num_graph())
    plt.show()
    return


class Graph:
    def __init__(self, lens, nums, R: float = 0.5):
        self.lens, self.nums, self.R = lens, nums, R
        self.graphs = {num: self.calc_graph(num) for num in nums}

    def calc_graph(self, n) -> NDArray:
        Y = np.zeros(len(self.lens), dtype=float)
        for i in range(len(self.lens)):
            s = RoundSeparator(self.R, self.lens[i], n)
            Y[i] = s.calc_clausing()
        return Y

    def plot_clausing(self, k: NDArray = None):
        for num in self.nums:
            plt.plot(self.lens, self.graphs[num], label=f"{num}")
        if k is not None and len(k):
            plt.plot(self.lens, k, label=f"теория")
        plt.xlabel("Длина канала L/d", size=19)
        plt.ylabel("Коэффициент Клаузинга", size=19)
        plt.legend(title="Количество колец")
        plt.grid()
        plt.show()
        return

    def calc_deviation(self, n, k: NDArray) -> NDArray:
        return (self.graphs[n] - k) / k * 100

    def plot_deviation(self, k: NDArray = None):
        if k is None or not len(k):
            raise ValueError("Invalid value of the k parameter")

        lens_min, deviation_min = [], []
        for num in self.nums:
            plt.plot(self.lens, self.calc_deviation(num, k), label=f"{num}")
        plt.xlabel("Длина канала L/d", size=19)
        plt.ylabel("Отклонение КК, %", size=19)
        plt.legend(title="Количество колец")
        plt.grid()
        plt.show()
        return

    def plot_min_pos(self, k: NDArray = None):
        def find_min():
            lens_min, mins = np.zeros(len(self.nums), dtype=float), np.zeros(len(self.nums), dtype=float)
            for i in range(len(self.nums)):
                deviation = self.calc_deviation(self.nums[i], k)
                index_min = int(np.where(deviation == np.min(deviation))[0])
                lens_min[i], mins[i] = self.lens[index_min], deviation[index_min]
            return lens_min, mins

        lens, mins = find_min()
        plt.plot(self.nums, lens)
        plt.xlabel("Количество колец", size=17)
        plt.ylabel("Длина канала L/d", size=17)
        plt.title("Положение точки минимума отклонения КК", size=18)
        plt.show()

        plt.plot(self.nums, mins)
        plt.xlabel("Количество колец", size=17)
        plt.ylabel("Отклонение КК, %", size=17)
        plt.title("Положение минимума отклонения КК", size=18)
        plt.show()
        return

    def plot_zero_pos(self, k: NDArray = None):
        def find_zero_pos(arr: NDArray):
            for j in range(len(arr)):
                if arr[j] >= 0.0 and j < len(arr) - 1:
                    return self.lens[j]

        zeros = np.array([find_zero_pos(self.calc_deviation(num, k)) for num in self.nums])
        interp = Interpolator(self.nums, zeros)
        print(*interp.calc_params())

        plt.errorbar(self.nums, zeros, yerr=interp.calc_error(), linestyle=" ")
        plt.plot(self.nums, zeros, marker="o", markersize=1.5, linestyle=" ", label="эксп. точки")
        plt.plot(self.nums, interp.calc_line(), label="аппроксимация")
        plt.xlabel("Количество колец n", size=17)
        plt.ylabel("Нуль L/d", size=17)
        plt.title("Положение нуля отклонения КК", size=18)
        plt.legend()
        plt.grid()
        plt.show()
        return

    def plot_deivation_n(self, l, k: NDArray = None):
        deviation = np.zeros(len(self.nums), dtype=float)
        l_pos = int(np.where(isclose(self.lens, l))[0])
        for i in range(len(self.nums)):
            d = self.calc_deviation(self.nums[i], k)[l_pos]
            deviation[i] = d
            print(i / 1000 * 100)
        plt.plot(self.nums, deviation)
        plt.xlabel(f"Количество колец при L/d = {l}")
        plt.ylabel("Отклонение КК, %")
        plt.grid()
        plt.show()
        return


n = np.array([1000])
x = list(theoretical_cc.keys())
x += list(range(550, 1050, 50))
values = list(theoretical_cc.values())
for i in range(len(theoretical_cc), len(x)):
    values.append(4 / 3 / x[i])  # from table
values = np.array(values)
g = Graph(x, n)
i = x.index(900)
print(g.calc_deviation(1000, values)[i])

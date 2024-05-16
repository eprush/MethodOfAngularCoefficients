from sep.round import RoundSeparator
from matplotlib import pyplot as plt
from numpy.typing import NDArray
from graphs import Graph
import numpy as np


def plot_num_of_cells(R, L, nums: NDArray[int]):
    def calc_dependence():
        Y = [0.0] * len(nums)
        for i in range(len(nums)):
            s = RoundSeparator(R, L, nums[i])
            coeffs = s.calc_ac()
            Y[i] = s.calc_clausing(coeffs)
        return np.array(Y)

    plt.xlabel("Количество ячеек n", size=17)
    plt.ylabel("Коэффициент Клаузинга", size=17)
    plt.plot(nums, calc_dependence())
    plt.grid()
    plt.show()


def plot_len(R, lens, nums, k: NDArray | None = None):
    def calc_dependence(n):
        Y = [0.0] * len(lens)
        for i in range(len(lens)):
            s = RoundSeparator(R, lens[i], n)
            coeffs = s.calc_ac()
            Y[i] = s.calc_clausing(coeffs)
        return np.array(Y)

    for num in nums:
        plt.plot(lens, calc_dependence(num), label=f"{num}")
    g = Graph()
    if k is not None and len(k):
        plt.plot(lens, k, label=f"эксперимент")
    plt.xlabel("Длина канала L/R", size=17)
    plt.ylabel("Коэффициент Клаузинга", size=17)
    plt.legend(title="Количество колец")
    plt.grid()
    plt.show()


def create_x() -> NDArray:
    X = np.linspace(0.1, 2, 20)
    X = X[:-1]
    X = list(X) + list(np.linspace(2, 5, 7))
    X = X[:-1]
    X = list(X) + list(np.linspace(5, 10, 6))
    return np.array(X)


x = np.arange(1, 31)
plot_num_of_cells(1, 2, x)

x = np.arange(1, 150)
#plot_len(1, x, np.array([3, 15, 150, 600]))
plot_len(0.5, create_x(), np.arange(1, 9, 2), Graph().k[1:])

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
        print(Y[-1])
        return np.array(Y)

    plt.title(f"Зависимость КК от количества ячеек L = {L}")
    plt.xlabel("Количество ячеек n")
    plt.ylabel("Коэффициент Клаузинга")
    plt.plot(nums, calc_dependence())
    plt.grid()
    plt.show()


x = np.arange(1, 31)
plot_num_of_cells(1, 2, x)


def plot_len(R, lens, nums):
    def calc_dependence(n):
        Y = [0.0] * len(lens)
        for i in range(len(lens)):
            s = RoundSeparator(R, lens[i], n)
            coeffs = s.calc_ac()
            Y[i] = s.calc_clausing(coeffs)
        print(Y[-1])
        return np.array(Y)

    for num in nums:
        plt.plot(lens, calc_dependence(num), label=f"{num}")
    g = Graph()
    plt.plot(lens, g.k[1:], label=f"эксперимент")
    plt.title("Зависимость КК от длина канала")
    plt.xlabel("Длина канала L/R")
    plt.ylabel("Коэффициент Клаузинга")
    plt.legend()
    plt.grid()
    plt.show()


#x = np.arange(1, 201)
#plot_len(1, x, np.array([2, 20, 200, 1000, 2000]))


def create_x() -> NDArray:
    X = np.linspace(0.1, 2, 20)
    X = X[:-1]
    X = list(X) + list(np.linspace(2, 5, 7))
    X = X[:-1]
    X = list(X) + list(np.linspace(5, 10, 6))
    return np.array(X)


plot_len(0.5, create_x(), np.arange(1, 10, 2))

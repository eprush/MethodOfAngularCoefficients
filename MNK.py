from math import sqrt
from numpy.typing import NDArray
import numpy as np


class Interpolator:
    def __init__(self, x: NDArray, y: NDArray):
        self.x, self.y = x, y

    def calc_params(self) -> tuple[float, float, float, float]:
        n = self.y.size
        aver_y, aver_x = np.mean(self.y), np.mean(self.x)
        aver_xy, aver_yy, aver_xx = np.mean(self.x * self.y), np.mean(self.y ** 2), np.mean(self.x ** 2)
        A = (aver_xy - aver_x * aver_y) / (aver_xx - aver_x ** 2)
        B = aver_y - A * aver_x
        err_A = sqrt(((aver_yy - aver_y ** 2) / (aver_xx - aver_x ** 2) - A ** 2) / n)
        err_B = err_A * sqrt(aver_xx - aver_x ** 2)
        return A, B, err_A, err_B

    def calc_line(self):
        a, b, *_ = self.calc_params()
        return a * self.x + b

    def calc_error(self):
        *_, err_a, err_b = self.calc_params()
        return np.sqrt((self.x * err_a) ** 2 + err_b ** 2)

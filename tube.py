from sep.rectangular import RectangleSeparator
from typing import Sequence
from decimal import Decimal
import numpy as np

Matrix_ac = Sequence[Sequence[Sequence[Sequence]]]
Center = np.ndarray
Sle = np.ndarray


def calc_elementary(center_i: Center, center_j: Center, normal_i: Center, normal_j: Center, F_j: Decimal) -> Decimal:
    # F_j - the area of one collector cell.
    r_vector = np.array(list(map(Decimal, center_j))) - np.array(list(map(Decimal, center_i)))
    r: Decimal = np.linalg.norm(r_vector)
    if not (r > 0):
        return Decimal(0.0)
    n_i, n_j = np.linalg.norm(normal_i), np.linalg.norm(normal_j)
    cos_i = abs(np.dot(normal_i, r_vector)) / (r * n_i)
    cos_j = abs(np.dot(normal_j, r_vector)) / (r * n_j)
    return cos_i * cos_j / (Decimal(np.pi) * r ** 2) * Decimal(F_j)


def flatten(arr: Sequence[Sequence]) -> Sequence:
    res = []
    try:
        for one_dimensional in arr:
            res += list(one_dimensional)
    except TypeError:
        print("the array introduced in flatten() was one-dimensional")
    return res


class Tube:
    def __init__(self, a, b, L, step_size: Decimal = Decimal(0.1)):
        self.separator = RectangleSeparator(a, b, L, step_size)

    def calc_angular_coeffs(self) -> Sle:
        sep = self.separator
        square = sep.step_size ** 2
        res = []
        for i, emitter in enumerate(sep):
            from_emitter = [0.0] * len(sep)
            normal_i = sep.find_normal(i)
            for j, collector in enumerate(sep):
                from_emitter[j] = calc_elementary(emitter, collector, normal_i, sep.find_normal(j), square)
            res.append(from_emitter)
        return np.array(res)

    def solve_sle(self, coeffs: Sle) -> Sequence:

        def create_sle() -> Sle:
            # unit matrix, because j-th equation is written for j-th flow
            return np.eye(len(self.separator)) - coeffs

        n = self.separator.find_num_cells(0)
        b = np.array([(1 / (self.separator.step_size * n) if i < n else 0) for i in range(len(self.separator))])
        return np.linalg.solve(create_sle(), b)

    def calc_clausing(self, coeffs: Sle) -> float:
        begin = self.separator.find_num_cells(0)
        end = begin + self.separator.find_num_cells(1)
        density_flows = self.solve_sle(coeffs)

        res = 0
        for i in range(len(self.separator)):
            if begin <= i < end:  # flow between cells of the same flat side
                continue
            res += sum([coeffs[i][j] * density_flows[i] for j in range(begin, end)])
        return res * self.separator.step_size ** 2

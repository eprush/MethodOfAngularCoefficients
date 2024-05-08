from sep.rectangular import RectangleSeparator
from calc_ac import calc_elementary
from typing import Sequence
from decimal import Decimal
import numpy as np

Matrix_ac = Sequence[Sequence[Sequence[Sequence]]]
Sle = np.ndarray


class Tube:
    def __init__(self, a, b, L, step_size: Decimal = Decimal("0.1")):
        self.separator = RectangleSeparator(a, b, L, step_size)

    def calc_angular_coeffs(self) -> Sle:
        sep = self.separator
        square = sep.step_size ** 2
        res = [[Decimal("0.0")] for _ in range(len(sep))]
        for i, emitter in enumerate(sep):
            from_emitter = [Decimal("0.0")] * len(sep)
            normal_i = sep.find_normal(i)
            emitter = np.array(emitter)
            for j, collector in enumerate(sep):
                collector = np.array(collector)
                from_emitter[j] = calc_elementary(emitter, collector, normal_i, sep.find_normal(j), square)
            res[i] = from_emitter
        return np.array(res)

    def solve_sle(self, coeffs: Sle) -> Sequence:

        def create_sle() -> Sle:
            # unit matrix, because j-th equation is written for j-th flow
            return np.eye(len(self.separator), dtype=Decimal) - coeffs

        n = self.separator.find_num_cells(0)
        b = np.array([Decimal("1.0") if i < n else Decimal("0.0") for i in range(len(self.separator))]) / n
        return np.linalg.solve(create_sle(), b)

    def calc_clausing(self, coeffs: Sle) -> Decimal:
        begin = self.separator.find_num_cells(0)
        end = begin + self.separator.find_num_cells(1)
        density_flows = self.solve_sle(coeffs)

        res = 0
        for i in range(len(self.separator)):
            if begin <= i < end:  # flow between cells of the same flat side
                continue
            res += sum([coeffs[i][j] * density_flows[i] for j in range(begin, end)])
        return res * self.separator.step_size ** 2

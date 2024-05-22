import numpy as np
from numpy.typing import NDArray


class RoundSeparator:
    def __init__(self, R: float, L: float, count_cells: int):
        self.R, self.L = R, L
        self._count_cells = count_cells

    def calc_ac(self) -> NDArray:
        phi_00 = phi_11 = 0.0
        s = self.L / self._count_cells
        phi_01 = phi_10 = 1.0 / (2.0 * self.R ** 2) * (s ** 2 + 2.0 * self.R ** 2
                                                       - s * (s ** 2 + 4.0 * self.R ** 2) ** 0.5)
        phi_02 = phi_12 = 1.0 - phi_00 - phi_10
        phi_20 = phi_21 = phi_02 * self.R / (2.0 * s)
        phi_22 = 1.0 - phi_20 - phi_21
        return np.array([[phi_00, phi_01, phi_02], [phi_10, phi_11, phi_12], [phi_20, phi_21, phi_22]],
                        dtype=float)

    def solve_sle(self, coeffs: NDArray) -> NDArray:
        def fill_sle(i):
            sle[i][i] = 1.0
            sle[i][i - 3] = -coeffs[0][1]
            sle[i][i - 1] = -coeffs[2][1]

            if i == 0:
                # the entrance section of the first ring
                sle[0] = [0.0] * 3 * n
                sle[0][0] = 1.0
            if i < 3 * (n - 1):
                sle[i + 1][i + 1] = 1.0
                sle[i + 1][i + 1 + 3] = -coeffs[1][0]
                sle[i + 1][i + 1 + 4] = -coeffs[2][0]
            else:
                # the output section of the last ring
                sle[3 * n - 2][3 * n - 2] = 1.0

            sle[i + 2][i] = -coeffs[0][2]
            sle[i + 2][i + 1] = -coeffs[1][2]
            sle[i + 2][i + 2] = 1.0 - coeffs[2][2]

        n = self._count_cells
        sle = np.zeros((3*n, 3*n), dtype=float)
        for j in range(0, 3 * n, 3):
            fill_sle(j)
        b = np.zeros(3*n, dtype=float)
        b[0] = 1.0  # the input flow
        return np.linalg.solve(sle, b)

    def calc_clausing(self, coeffs = None) -> float:
        if coeffs is None:
            coeffs = self.calc_ac()
        n = self._count_cells
        flows = self.solve_sle(coeffs)
        # because coeffs[1][1] == 0
        return flows[3 * n - 1] * coeffs[2][1] + flows[3 * n - 3] * coeffs[0][1]

from numpy.typing import NDArray
import numpy as np


class RoundSeparator:
    def __init__(self, R: float, L: float, count_cells: int):
        self.R, self.L = R, L
        self._count_cells = count_cells

    def calc_ac(self) -> NDArray:
        phi_00 = phi_11 = 0.0
        s = self.L / float(self._count_cells)
        phi_01 = phi_10 = 1.0 / (2.0 * self.R ** 2) * (s ** 2 + 2.0 * self.R ** 2
                                                       - s * (s ** 2 + 4.0 * self.R ** 2) ** 0.5)
        phi_02 = phi_12 = 1.0 - phi_00 - phi_10
        phi_20 = phi_21 = phi_02 * self.R / (2.0 * s)
        phi_22 = 1.0 - phi_20 - phi_21
        return np.array([[phi_00, phi_01, phi_02], [phi_10, phi_11, phi_12], [phi_20, phi_21, phi_22]],
                        dtype=float)

    def solve_sle(self, coeffs: NDArray) -> NDArray:
        if not coeffs.size:
            coeffs = self.calc_ac()
        n = self._count_cells

        def create_sle() -> NDArray:
            sle = [[0.0] * 3 * n for _ in range(3 * n)]
            for i in range(0, 3 * n, 3):
                sle[i][i] = 1.0
                sle[i][i - 3] = -coeffs[0][1]
                sle[i][i - 1] = -coeffs[2][1]

                if i < 3 * (n - 1):
                    sle[i + 1][i + 1] = 1.0
                    sle[i + 1][i + 1 + 3] = -coeffs[1][0]
                    sle[i + 1][i + 1 + 4] = -coeffs[2][0]
                else:
                    sle[3 * n - 2] = [1.0 if j == 3 * n - 2 else 0.0 for j in range(3 * n)]

                sle[i + 2][i] = -coeffs[0][2]
                sle[i + 2][i + 1] = -coeffs[1][2]
                sle[i + 2][i + 2] = 1.0 - float(coeffs[2][2])

                if i == 0:
                    sle[0] = [1.0 if j == 0 else 0.0 for j in range(3 * n)]
            return np.array(sle, dtype=float)

        b = np.array([1.0 if j == 0 else 0.0 for j in range(3 * n)], dtype=float)
        return np.linalg.solve(create_sle(), b)

    def calc_clausing(self, coeffs) -> float:
        n = self._count_cells
        flows = self.solve_sle(coeffs)
        return flows[3 * n - 1] * coeffs[2][1] + flows[3 * n - 3] * coeffs[0][1]
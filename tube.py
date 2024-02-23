from rectangular.rectangular import RectangleSeparator
from typing import Optional, Sequence
import numpy.typing as npt
import numpy as np

Matrix_ac = Sequence[Sequence[Sequence[Sequence]]]
Center = npt.ArrayLike
Sle = npt.ArrayLike


def calc_elementary_ac(center_i: Center, center_j: Center, normal_i: np.ndarray, normal_j: np.ndarray, F_j):
    # F_j - the area of one collector cell.
    r_vector = center_j - center_i
    r = np.linalg.norm(r_vector)
    n_i, n_j = np.linalg.norm(normal_i), np.linalg.norm(normal_j)

    cos_i = abs(np.dot(normal_i, r_vector)) / (r * n_i)
    cos_j = abs(np.dot(normal_j, r_vector)) / (r * n_j)
    return cos_i * cos_j / (np.pi * r ** 2) * F_j


class Tube:
    def __init__(self, separator: Optional[RectangleSeparator]):
        self.separator = separator

    def calc_angular_coeffs(self) -> Sequence[Sequence[Sequence[Sequence]]]:
        sep = self.separator
        from_output_side = []
        for output_side in range(sep.SIDES):
            from_emitter = []
            for emitter in sep.breaks[output_side]:
                def calc_for_each_collector(side: int) -> Sequence[float]:
                    if side == output_side:
                        # cells on the same side have angular coeffs equal to 0
                        return [0] * sep.find_num_cells(side)
                    return [
                        calc_elementary_ac(emitter, collector, sep.normals[output_side], sep.normals[side],
                                           sep.cell) for collector in sep.breaks[side]]

                to_input_side = [calc_for_each_collector(input_side) for input_side in range(sep.SIDES)]
                from_emitter.append(to_input_side)
            from_output_side.append(from_emitter)
        return from_output_side

    def find_pos(self, s: int) -> int:
        return sum([self.separator.find_num_cells(i) for i in range(s)])

    def create_sle(self) -> Sle:
        # builds a system of linear equations 2.1
        def straighten_out(arr: Sequence[Sequence[Sequence[Sequence]]]) -> Sequence[Sequence]:
            return [[np.ravel(np.array(arr[i][j])) for j in range(self.separator.find_num_cells(i))]
                    for i in range(self.separator.SIDES)]  # straightened in 3d and 4th dimensions multidimensional list

        total_number = self.separator.find_total_num()
        sle = np.eye(total_number)  # the unit matrix, because the j-th equation is written for the j-th flow
        coeffs = straighten_out(self.calc_angular_coeffs())

        def fill_sle():
            for output_side in range(2, self.separator.SIDES):
                column_i = self.find_pos(output_side)
                for emitter_i in range(self.separator.find_num_cells(output_side)):
                    for row_i in range(total_number):
                        sle[row_i][column_i] -= coeffs[output_side][emitter_i][row_i]
                    column_i += 1
            return

        fill_sle()
        return sle

    def solve_sle(self, sle: Sle) -> Sequence:
        b = np.array([1 / self.separator.cell if i < self.separator.find_num_cells(0) else 0
                      for i in range(self.separator.find_total_num())])
        return np.linalg.solve(sle, b)

    def calc_clausing(self, sle: Sle):
        density_flows = self.solve_sle(sle)
        output_side = 1
        res = 0
        for side in range(self.separator.SIDES):
            if side == output_side:
                break

            pos = self.find_pos(side)
            for collector_i in range(self.separator.find_num_cells(output_side)):
                res += sum([sle[side][emitter_i][output_side][collector_i] * density_flows[pos + emitter_i]
                            for emitter_i in range(self.separator.find_num_cells(side))])
        return res * self.separator.cell


def check_solution(sle, x, b):
    return np.allclose(np.dot(sle, x), b)

from typing import Optional, Sequence, Iterable
from rectangular import RectangleSeparator
import numpy.typing as npt
import numpy as np

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

    def calc_angular_coeffs(self) -> Sequence[Sequence[Sequence[Iterable]]]:
        sep = self.separator
        from_output_side = []
        for output_side in range(sep.SIDES):
            from_emitter = []
            for emitter in sep.breaks[output_side]:
                def calc_for_each_collector(side: int) -> Iterable[float]:
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

    def create_sle(self) -> Sle:
        # builds a system of linear equations 2.1
        def straighten_out(arr: Sequence) -> Sequence:
            return [[np.ravel(np.array(arr[i][j])) for j in range(self.separator.find_num_cells(i))]
                    for i in range(self.separator.SIDES)]  # straightened in 3d and 4th dimensions multidimensional list

        total_number = self.separator.find_total_num()
        sle = np.eye(total_number)  # the unit matrix, because the j-th equation is written for the j-th flow
        coeffs = straighten_out(self.calc_angular_coeffs())

        def fill_sle():
            def find_column(side: int) -> int:
                # a temporary solution
                return sum([self.separator.find_num_cells(i) for i in range(side)])

            for output_side in range(2, self.separator.SIDES):
                column_i = find_column(output_side)
                for emitter_i in range(self.separator.find_num_cells(output_side)):
                    for row_i in range(total_number):
                        sle[row_i][column_i] -= coeffs[output_side][emitter_i][row_i]
                    column_i += 1
            return

        fill_sle()
        return sle

    def calc_flows(self):
        b = np.array([1 if i < self.separator.find_num_cells(0) else 0 for i in range(self.separator.find_total_num())])
        # 1 or other number?
        return np.linalg.solve(self.create_sle(), b)

    def calc_clausing(self):
        pass
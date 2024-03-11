from rectangular.rectangular import RectangleSeparator
from typing import Optional, Sequence
import numpy.typing as npt
import numpy as np

Matrix_ac = Sequence[Sequence[Sequence[Sequence]]]
Center = npt.ArrayLike
Sle = np.ndarray


def calc_elementary_ac(center_i: Center, center_j: Center, normal_i: np.ndarray, normal_j: np.ndarray, F_j) -> float:
    # F_j - the area of one collector cell.
    r_vector = center_j - center_i
    r = np.linalg.norm(r_vector)
    n_i, n_j = np.linalg.norm(normal_i), np.linalg.norm(normal_j)

    cos_i = abs(np.dot(normal_i, r_vector)) / (r * n_i)
    cos_j = abs(np.dot(normal_j, r_vector)) / (r * n_j)
    return cos_i * cos_j / (np.pi * r ** 2) * F_j


def flatten(arr: Sequence[Sequence]) -> npt.ArrayLike:
    res = []
    try:
        for one_dimensional in arr:
            res += list(one_dimensional)
    except TypeError:
        print(f"the array introduced in flatten() was one-dimensional")
    return np.array(res)


class Tube:
    def __init__(self, separator: Optional[RectangleSeparator]):
        self.separator = separator

    def calc_angular_coeffs(self) -> Sle:
        def convert(arr: Matrix_ac) -> Sle:
            # begin with arr[first][second][third][fourth]
            max_len, total_num = self.separator.find_max_num(), self.separator.find_total_num()
            sides = self.separator.SIDES
            buffer = [[flatten(arr[i][j]) if j < len(arr[i]) else [0] * total_num for j in range(max_len)]
                      for i in range(sides)]  # arr[first][new_second][third + fourth]
            buffer = np.transpose(np.array(buffer))  # arr[third + fourth][new_second][first]
            res = []
            for i in range(total_num):
                internal_arr = np.transpose(buffer[i])  # arr[first][new_second]
                internal_arr = [internal_arr[j][:self.separator.find_num_cells(j)] for j in range(sides)]
                # arr[first][second]
                internal_arr = flatten(internal_arr)  # arr[first + second]
                res.append(internal_arr)
            return np.transpose(np.array(res))  # arr[first + second][third + fourth]

        sep = self.separator
        from_output_side = []
        for output_side in range(sep.SIDES):
            from_emitter = []

            def calc_for_each_collector(side: int, center: Center) -> Sequence[float]:
                if side == output_side:
                    # cells on the same side have angular coeffs equal to 0
                    return [0] * sep.find_num_cells(side)
                return [calc_elementary_ac(center, collector, sep.normals[output_side], sep.normals[side],
                                           sep.cell) for collector in sep.breaks[side]]

            for emitter in sep.breaks[output_side]:
                to_input_side = [calc_for_each_collector(input_side, emitter) for input_side in range(sep.SIDES)]
                from_emitter.append(to_input_side)
            from_output_side.append(from_emitter)

        return convert(from_output_side)

    def solve_sle(self, coeffs: Sle) -> Sequence:
        def create_sle() -> Sle:
            # unit matrix, because j-th equation is written for j-th flow
            return np.eye(self.separator.find_total_num()) - coeffs

        n = self.separator.find_num_cells(0)
        b = np.array([(1 / (self.separator.cell * n) if i < n else 0) for i in range(self.separator.find_total_num())])
        return np.linalg.solve(create_sle(), b)

    def calc_clausing(self, coeffs: Sle) -> float:
        begin = self.separator.find_num_cells(0)
        end = begin + self.separator.find_num_cells(1)
        density_flows = self.solve_sle(coeffs)

        res = 0
        for i in range(self.separator.find_total_num()):
            if begin <= i < end:  # flow between cells of the same flat side
                continue
            res += sum([coeffs[i][j] * density_flows[i] for j in range(begin, end)])
        return res * self.separator.cell


rect = RectangleSeparator(1, 5, 1, 0.01)
t = Tube(rect)
c = t.calc_angular_coeffs()
print(t.calc_clausing(c), "\n")

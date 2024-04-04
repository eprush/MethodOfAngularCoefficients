from typing import Sequence, List
from decimal import Decimal
import functools
import numpy as np

Center = np.ndarray


def multiply(arr: Sequence):
    return functools.reduce(lambda a, b: a * b, arr)


def create_empty_centers(size: int) -> List:
    return [np.zeros(3)] * size


class RectangleSeparator:
    """0 - the entrance, 1 - the output, 2 - lower, 3 - upper, 4 - back, 5 - front sides"""
    SIDES = 6
    normals = [[0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1], [1, 0, 0], [-1, 0, 0]]
    for i in range(SIDES):
        normals[i] = list(map(Decimal, normals[i]))
    normals = np.array(normals)

    def __init__(self, a, b, L, step_size: Decimal):
        self.a, self.b, self.L, self.step_size = a, b, L, Decimal(step_size)
        self._steps: tuple[tuple] = self.calc_steps()
        self._breaks = self.separate()
        return

    def __len__(self) -> int:
        return 2 * sum(list(map(multiply, self._steps)))

    def __getitem__(self, item):
        return self._breaks[item]

    def __iter__(self):
        return iter(self._breaks)

    def calc_steps(self) -> tuple:
        res = np.array([[self.a, self.b], [self.a, self.L], [self.L, self.b]]) / self.step_size
        res = tuple(map(lambda x: (int(x[0]), int(x[1])), res))
        return res

    def separate(self) -> Sequence[np.ndarray]:
        """splits each pair of sides into cells"""
        coord = (float(self.L), float(self.b), float(self.a))
        separation: Sequence[np.ndarray] = []
        s_coord = 0.0

        for couple_side in range(RectangleSeparator.SIDES // 2):
            b_coord, (count_1, count_2) = coord[couple_side], self._steps[couple_side]
            s_res = create_empty_centers(count_1 * count_2)
            b_res = s_res.copy()
            index = 0

            for i in range(count_1):
                coord_1 = self.step_size / 2 + self.step_size * i
                for j in range(count_2):
                    coord_2 = self.step_size / 2 + self.step_size * j
                    # take into account the symmetry
                    if not i:
                        centers = (np.array([coord_1, s_coord, coord_2]), np.array([coord_1, b_coord, coord_2]))
                    elif i == 1:
                        centers = (np.array([coord_1, coord_2, s_coord]), np.array([coord_1, coord_2, b_coord]))
                    else:
                        centers = (np.array([s_coord, coord_1, coord_2]), np.array([b_coord, coord_1, coord_2]))

                    s_res[index], b_res[index] = centers
                    index += 1

            separation += s_res + b_res
        return separation

    def find_num_cells(self, side: int) -> int:
        return multiply(self._steps[side // 2])

    def find_normal(self, item) -> np.ndarray:
        side_nums, side = 0, -1
        while item >= side_nums:
            side += 1
            side_nums += self.find_num_cells(side)
            if side >= RectangleSeparator.SIDES:
                raise IndexError(f"index {item} is out of range {len(self)}")
        return RectangleSeparator.normals[side]

    def find_max_num(self):
        return max([self.find_num_cells(i) for i in range(self.SIDES)])

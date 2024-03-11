from typing import Iterable, Sequence, Sized
from numpy.typing import ArrayLike
import numpy as np

Center = ArrayLike


def create_empty_centers(size: int) -> ArrayLike[Center]:
    return np.zeros((size, 3))


class RectangleSeparator:
    normals = (np.array([0, 1, 0]), np.array([0, -1, 0]), np.array([0, 0, -1]), np.array([1, 0, 0]),
               np.array([0, 0, 1]), np.array([-1, 0, 0]))
    SIDES = 6

    def __init__(self, a, b, L, cell: float = 0.01):
        self.a, self.b, self.L, self.cell = a, b, L, cell
        self.breaks = self.separate()

    def separate(self) -> Sized | Sequence:
        """splits each pair of sides into cells.
        0-the entrance, 1-the output sides; 2-upper, 4-lower sides.
        if you look in the direction from 0 to 1, then 2,3,4 and 5 sides are numbered counterclockwise"""

        step = np.sqrt(self.cell)
        separation = [[]] * self.SIDES

        def break_01() -> tuple[Iterable[Center], Iterable[Center]]:
            y_0, y_1 = 0.0, float(self.L)
            l_1, l_2 = int(self.a / step), int(self.b / step)
            res_0 = create_empty_centers(l_1 * l_2)
            res_1 = res_0.copy()

            index = 0
            for i in range(l_1):
                x = step / 2 + step * i
                for j in range(l_2):
                    z = step / 2 + step * j
                    center_0, center_1 = np.array([x, y_0, z]), np.array([x, y_1, z])
                    res_0[index], res_1[index] = center_0, center_1
                    index += 1
            return res_0, res_1

        def break_24() -> tuple[Iterable[Center], Iterable[Center]]:
            z_2, z_4 = float(self.b), 0.0
            l_1, l_2 = int(self.a / step), int(self.L / step)
            res_2 = create_empty_centers(l_1 * l_2)
            res_4 = res_2.copy()

            index = 0
            for i in range(l_1):
                x = step / 2 + step * i
                for j in range(l_2):
                    y = step / 2 + step * j
                    center_2, center_4 = np.array([x, y, z_2]), np.array([x, y, z_4])
                    res_2[index], res_4[index] = center_2, center_4
                    index += 1
            return res_2, res_4

        def break_35() -> tuple[Iterable[Center], Iterable[Center]]:
            x_3, x_5 = 0.0, float(self.a)
            l_1, l_2 = int(self.L / step), int(self.b / step)
            res_3 = create_empty_centers(l_1 * l_2)
            res_5 = res_3.copy()

            index = 0
            for i in range(l_1):
                y = step / 2 + step * i
                for j in range(l_2):
                    z = step / 2 + step * j
                    center_3, center_5 = np.array([x_3, y, z]), np.array([x_5, y, z])
                    res_3[index], res_5[index] = center_3, center_5
                    index += 1
            return res_3, res_5

        try:
            separation[0], separation[1] = break_01()
            separation[2], separation[4] = break_24()
            separation[3], separation[5] = break_35()
            return separation
        except ValueError as err:
            print("ValueError:", err)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

    def find_num_cells(self, side: int) -> int:
        # i - the number of the desired emitter
        return len(self.breaks[side])

    def find_max_num(self):
        return max([self.find_num_cells(i) for i in range(self.SIDES)])

    def find_total_num(self) -> int:
        return sum([self.find_num_cells(side) for side in range(self.SIDES)])

    def find_pos(self, s: int) -> int:
        return sum([self.find_num_cells(i) for i in range(s)])

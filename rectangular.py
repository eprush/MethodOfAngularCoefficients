import math
import numpy as np


# УГЛОВЫЕ КОЭФФИЦИЕНТЫ
def scalar_prod(v_1, v_2):
    v_1, v_2 = np.array(v_1), np.array(v_2)
    return np.dot(v_1, v_2)


def module(v):
    return math.sqrt(scalar_prod(v, v))


def elementary(center_i: list, center_j: list, normal_i: list, normal_j: list, F_j):
    # F_j - площадь одной ячейки коллектора.
    center_i, center_j = np.array(center_i), np.array(center_j)
    r, n_i, n_j = module(center_i - center_j), module(normal_i), module(normal_j)

    cos_i = abs(scalar_prod(normal_i, center_j - center_i)) / (r * n_i)
    cos_j = abs(scalar_prod(normal_j, center_i - center_j)) / (r * n_j)
    return cos_i * cos_j / (math.pi * r ** 2) * F_j


def local(center_i, centers_j, normal_i, normal_j, F_j):
    return sum([elementary(center_i, center, normal_i, normal_j, F_j) for center in centers_j])


def emitter_to_collector(centers_i, centers_j, normal_i, normal_j, F_i, F_j):
    # F_i - площадь одной ячейки эмиттера.
    return sum([local(center, centers_j, normal_i, normal_j, F_j) for center in centers_i]) * F_i


# РАЗБИЕНИЕ
# функции разбиения каждой отдельной поверхности на ячейки.
# 1-входное, 2-выходное сечения.
# 3-верхняя, 5-нижняя грани.
# если смотреть в направлении от 1 к 2, то
# 3,4,5 и 6 грани пронумерованы по часовой стрелке.
def break_1(a, b, cell, s) -> list:
    cell = math.sqrt(cell)
    l_1 = int(a / cell)
    l_2 = int(b / cell)
    res = []
    for i in range(l_1):
        x = round(cell / 2 + cell * i, 5)
        for j in range(l_2):
            z = round(cell / 2 + cell * j, 5)
            center = [x, 0, z]
            res.append(center)
    return res


def break_2(a, b, cell, s) -> list:
    cell = math.sqrt(cell)
    l_1 = int(a / cell)
    l_2 = int(b / cell)
    res = []
    for i in range(l_1):
        x = round(cell / 2 + cell * i, 5)
        for j in range(l_2):
            z = round(cell / 2 + cell * j, 5)
            center = [x, s, z]
            res.append(center)
    return res


def break_3(a, b, cell, s) -> list:
    res = []
    cell = math.sqrt(cell)
    l_1 = int(a / cell)
    l_2 = int(s / cell)
    for i in range(l_1):
        x = round(cell / 2 + cell * i, 5)
        for j in range(l_2):
            y = round(cell / 2 + cell * j, 5)
            center = [x, y, b]
            res.append(center)
    return res


def break_4(a, b, cell, s) -> list:
    res = []
    cell = math.sqrt(cell)
    l_1 = int(s / cell)
    l_2 = int(b / cell)
    for i in range(l_1):
        y = round(cell / 2 + cell * i, 5)
        for j in range(l_2):
            z = round(cell / 2 + cell * j, 5)
            center = [0, y, z]
            res.append(center)
    return res


def break_5(a, b, cell, s) -> list:
    res = []
    cell = math.sqrt(cell)
    l_1 = int(a / cell)
    l_2 = int(s / cell)
    for i in range(l_1):
        x = round(cell / 2 + cell * i, 5)
        for j in range(l_2):
            y = round(cell / 2 + cell * j, 5)
            center = [x, y, 0]
            res.append(center)
    return res


def break_6(a, b, cell, s) -> list:
    res = []
    cell = math.sqrt(cell)
    l_1 = int(s / cell)
    l_2 = int(b / cell)
    for i in range(l_1):
        y = round(cell / 2 + cell * i, 5)
        for j in range(l_2):
            z = round(cell / 2 + cell * j, 5)
            center = [a, y, z]
            res.append(center)
    return res


# площади "уникальных" поверхностей - area_1 == area_2 итд.
def area_1(a, b, s):
    return a * b


def area_3(a, b, s):
    return a * s


def area_4(a, b, s):
    return s * b


# ПРОВОДИМОСТЬ
# ф-ция, заменяющая j-й столбец матрицы A.
def change_column(A, j: int = 0):
    new_A = A.copy()
    new_A[0][j] = 1
    for i in range(1, len(new_A)):
        new_A[i][j] = 0
    return new_A


class Rectangular:
    def __init__(self, a, b, L, cell=0.01):
        self.a = a
        self.b = b
        self.L = L
        self.cell = cell
        self.normals = [[0, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 0, 1], [1, 0, 0]]
        self.breaks = [break_1, break_2, break_3, break_4, break_5, break_6]

        self.areas = [area_1, area_1, area_3, area_4, area_3, area_4]
        for i in range(6):
            self.areas[i] = self.areas[i](a, b, L)
            self.breaks[i] = self.breaks[i](a, b, cell, L)
        return

    def angular_coeff(self, i, j):
        # i - номер эмиттера   от 1 до 6.
        # j - номер коллектора от 1 до 6.
        # cell - размер ячейки.
        i -= 1  # это - номер эмиттера   в массивах.
        j -= 1  # это - номер коллектора в массивах.

        # параметры коллектора:
        collectors = self.breaks[j]
        normal_j = self.normals[j]

        # параметры эмиттера:
        emitters = self.breaks[i]
        normal_i = self.normals[i]
        area_i = self.areas[i]
        return emitter_to_collector(emitters, collectors, normal_i, normal_j, self.cell, self.cell) / area_i

    def check_add(self, i, j):
        # i - номер эмиттера   от 1 до 6.
        # j - номер коллектора от 1 до 6.
        # cell - размер ячейки.
        i -= 1  # это - номер эмиттера   в массивах.
        j -= 1  # это - номер коллектора в массивах.

        # параметры коллектора:
        collectors = self.breaks[j]
        normal_j = self.normals[j]

        # параметры эмиттера:
        emitters = self.breaks[i]
        normal_i = self.normals[i]
        area_i = self.areas[i]
        #изменили порядок суммирования
        #по сравнению с self.angular_coeff(i,j)
        return emitter_to_collector(collectors, emitters, normal_j, normal_i, self.cell, self.cell) / area_i

    def matrix(self):
        res = []  # будущая матрица УК.
        line = [0] * 7  # текущий столбец матрицы.
        for i in range(1, 7):
            res.append(np.array(line))
            line = [0]
            for j in range(1, 7):
                if j == i:
                    line.append(0)
                else:
                    line.append(self.angular_coeff(i, j))
        res.append(np.array(line))
        return np.array(res)

    def clausing(self):
        phi = self.matrix()
        # СЛУ
        sle = [[1, 0, 0],
               [-phi[1][3], 1 - phi[5][3], -2 * phi[4][3]],
               [-phi[1][4], -2 * phi[3][4], 1 - phi[6][4]]]
        sle = np.array(sle)
        delta = np.linalg.det(sle)
        q = []  # [Q_1, Q_3, Q_4]
        # метод Крамера.
        for j in range(3):
            new_sle = change_column(sle, j)
            delta_j = np.linalg.det(new_sle)
            q.append(delta_j / delta)
        res = phi[1][2] * q[0]
        res += 2 * phi[3][2] * q[1]
        res += 2 * phi[4][2] * q[2]
        return res
